import xml.etree.ElementTree as ET
from datetime import datetime

def create_rss_feed(papers):
    # Create root RSS element with ALL needed namespaces
    rss = ET.Element('rss', {
        'version': '2.0',
        'xmlns:arxiv': 'http://arxiv.org/schemas/atom',
        'xmlns:atom': 'http://www.w3.org/2005/Atom',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
    })
    
    # Create channel element
    channel = ET.SubElement(rss, 'channel')
    
    # Add channel metadata
    ET.SubElement(channel, 'title').text = 'cs updates on arXiv.org'
    ET.SubElement(channel, 'link').text = 'http://rss.arxiv.org/rss/cs'
    ET.SubElement(channel, 'description').text = 'cs updates on the arXiv.org e-print archive.'
    
    # Add atom:link
    atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
    atom_link.set('href', 'http://rss.arxiv.org/rss/cs')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Add other channel elements
    ET.SubElement(channel, 'docs').text = 'http://www.rssboard.org/rss-specification'
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    ET.SubElement(channel, 'managingEditor').text = 'rss-help@arxiv.org'
    ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0500')
    # Add items
    for paper in papers:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = paper['title']
        ET.SubElement(item, 'link').text = paper['link']
        ET.SubElement(item, 'description').text = paper['summary'] + "\n" + paper['explanation'] + "\n" + paper['description'] if "summary" in paper and "explanation" in paper else paper['description']
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"oai:arXiv.org:{paper['link'].split('/')[-1]}"
        ET.SubElement(item, 'category').text = 'cs.AI'
        ET.SubElement(item, 'pubDate').text = paper['date_published']
        ET.SubElement(item, '{http://arxiv.org/schemas/atom}announce_type').text = 'new'
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}rights').text = 'http://creativecommons.org/licenses/by/4.0/'
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = paper['authors']
    
    return rss