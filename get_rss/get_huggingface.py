import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json

from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
from xml.etree import ElementTree as ET

from utils import CustomLogger, create_rss_feed, RedisClient
from llm import PaperJudgeRequest
from config import PAPER_EXPIRE_TIME, HUGGINFACE_URL, REDIS_DB_HUGGINFACE

logger = CustomLogger()
pjr = PaperJudgeRequest()
rc = RedisClient(db=REDIS_DB_HUGGINFACE)  # 使用不同的db以区分arxiv的数据

def fetch_huggingface_papers():
    """获取Hugging Face论文列表"""
    try:
        page = requests.get(HUGGINFACE_URL)
        page.raise_for_status()
        return page.content
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Hugging Face papers: {e}")
        return None

def extract_paper_details(url):
    """提取论文的详细信息"""
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        
        abstract_div = soup.find("div", {"class": "pb-8 pr-4 md:pr-16"})
        abstract = abstract_div.text if abstract_div else ""
        
        time_element = soup.find("time")
        datetime_str = time_element.get("datetime") if time_element else None
        if datetime_str and not datetime_str.endswith("Z"):
            datetime_str = f"{datetime_str}Z"
            
        if abstract.startswith("Abstract\n"):
            abstract = abstract[len("Abstract\n"):]
        abstract = abstract.replace("\n", " ").strip()
        
        return abstract, datetime_str
    except Exception as e:
        logger.error(f"Failed to extract details for {url}: {e}")
        return "", None

def parse_huggingface_page(html_content):
    """解析Hugging Face页面内容"""
    papers = []
    
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        h3s = soup.find_all("h3")
        
        for h3 in h3s:
            a = h3.find("a")
            if not a:
                continue
                
            title = a.text
            link = f"https://huggingface.co{a['href']}"
            
            # 检查Redis缓存
            if rc.get_paper(link) and rc.get_paper(link)['is_qualified'] == 'yes':
                logger.debug(f"Paper {link} already exists in redis.")
                papers.append(rc.get_paper(link))
                continue
            
            abstract, date_published = extract_paper_details(link)
            
            paper = {
                'title': title.strip(),
                'authors': '',  # HF页面可能需要额外解析作者信息
                'abstract': abstract,
                'link': link,
                'date_published': date_published,
                'description': abstract
            }
            
            # 使用AI判断论文相关性
            paper['is_qualified'], paper['explanation'], paper['summary'] = pjr.send_paper_judge_request(abstract)
            rc.set_paper(paper, PAPER_EXPIRE_TIME)

            logger.debug(f"Paper {link} is selected.")
            papers.append(paper)
                
    except Exception as e:
        logger.error(f"Failed to parse Hugging Face page: {e}")
    
    return papers

def get_huggingface_papers():
    """主函数：获取并处理Hugging Face论文"""
    # 获取页面内容
    html_content = fetch_huggingface_papers()
    if not html_content:
        return None
    
    # 解析论文信息
    papers = parse_huggingface_page(html_content)
    
    # 创建RSS feed
    rss = create_rss_feed(papers)
    
    # 创建XML字符串
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_str += ET.tostring(rss, encoding='unicode', method='xml')
    
    # 格式化XML
    dom = parseString(xml_str)
    dom.normalize()
    xml_str = dom.toprettyxml(indent="  ")
    
    # 保存到文件
    with open("feed/feed_hf.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
        logger.info(f"Feed saved to feed_hf.xml")
    
    with open("feed/feed_hf.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
        logger.info(f"Feed saved to feed_hf.json")

    return xml_str

if __name__ == "__main__":
    get_huggingface_papers()