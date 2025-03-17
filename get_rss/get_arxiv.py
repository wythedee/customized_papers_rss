import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import requests
from datetime import datetime

from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString

from llm import PaperJudgeRequest
from utils import CustomLogger, create_rss_feed, RedisClient
from config import PAPER_EXPIRE_TIME, PAPER_NUMBER, RSS_URL, REDIS_DB_ARXIV


logger = CustomLogger()
pjr = PaperJudgeRequest()
rc = RedisClient(db=REDIS_DB_ARXIV)

def fetch_arxiv_rss():
    # arXiv CS RSS feed URL
    url = RSS_URL
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
            logger.debug(f"Paper {link} already exists in redis.")
            if rc.get_paper(link)['is_qualified'] == 'yes':
                logger.debug(f"Paper {link} is qualified.")
                papers.append(rc.get_paper(link))
                count += 1
                continue
            else:
                logger.debug(f"Paper {link} is not qualified.")
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
            logger.debug(f"Paper {link} is selected.")
            papers.append(paper)
            count += 1
        else:
            logger.debug(f"Paper {link} is not related to Misinformation Detection.")
        

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
    with open("feed/feed_arxiv.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
        logger.info(f"Feed saved to feed_arxiv.xml")

    with open("feed/feed_arxiv.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
        logger.info(f"Feed saved to feed_arxiv.json")
        
    return xml_str

if __name__ == "__main__":  
    get_arxiv_rss()