from logger_config import CustomLogger
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from paper_judge_request import PaperJudgeRequest
from redis_client import RedisClient
from xml_tools import create_rss_feed
from xml.dom.minidom import parseString
from config import PAPER_EXPIRE_TIME, PAPER_NUMBER
import json

logger = CustomLogger()
pjr = PaperJudgeRequest()
rc = RedisClient(db=0)

def fetch_arxiv_rss():
    # arXiv CS RSS feed URL
    url = "http://rss.arxiv.org/rss/cs.AI"
    response = requests.get(url)
    return response.content

def parse_arxiv_feed(xml_content):
    # Parse XML content
    root = ET.fromstring(xml_content)
    papers = []

    namespaces = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    count = 0
    # Iterate through each item in the feed
    for item in root.findall('.//item'):
        if count >= PAPER_NUMBER:
            break
        # Extract basic information
        link = item.find('link').text

        if rc.get_paper(link):
            logger.info(f"Paper {link} already exists in redis.")
            if rc.get_paper(link)['is_qualified'] == 'yes':
                logger.info(f"Paper {link} is qualified.")
                papers.append(rc.get_paper(link))
                count += 1
                continue
            else:
                logger.info(f"Paper {link} is not qualified.")
                continue

        title = item.find('title').text
        description = item.find('description').text
        
        # Extract abstract from description
        abstract = description.split('Abstract: ')[-1] if 'Abstract: ' in description else ''
        
        # Extract authors
        authors = item.find('dc:creator', namespaces=namespaces)
        authors = authors.text if authors is not None else ''
        
        # Extract publication date
        pub_date = item.find('pubDate').text
        pub_date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
        pub_date_iso = pub_date_obj.isoformat()
        
        # Create paper dictionary
        paper = {
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'link': link,
            'date_published': pub_date,  # Keep original format
            'description': description,  # Keep full description
        }

        paper['is_qualified'], paper['explanation'], paper['summary'] = pjr.send_paper_judge_request(abstract)
        if paper['is_qualified'] is None:
            continue
        rc.set_paper(paper, PAPER_EXPIRE_TIME)
        if paper['is_qualified'] == 'yes' or paper['is_qualified'] == 'Yes':
            logger.info(f"Paper {link} is selected.")
            papers.append(paper)
            count += 1
        else:
            logger.info(f"Paper {link} is not related to Misinformation Detection.")
        

    return papers

def get_arxiv_rss():
    # Fetch RSS feed
    xml_content = fetch_arxiv_rss()
    
    # Parse feed and extract papers
    papers = parse_arxiv_feed(xml_content)
    
    # Create RSS feed
    rss = create_rss_feed(papers)
    
    # Create XML string with declaration
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_str += ET.tostring(rss, encoding='unicode', method='xml')

    dom = parseString(xml_str)
    dom.normalize()
    xml_str = dom.toprettyxml(indent="  ")
    
    # Save to file
    with open("feed_arxiv.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
        logger.info(f"Feed saved to feed_arxiv.xml")

    with open("feed_arxiv.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
        logger.info(f"Feed saved to feed_arxiv.json")
        
    return xml_str

if __name__ == "__main__":  
    get_arxiv_rss()