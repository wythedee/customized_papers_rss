from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from get_rss import get_arxiv_rss, get_huggingface_papers
from utils import CustomLogger

logger = CustomLogger()

app = Flask(__name__)
scheduler = BackgroundScheduler()

def fetch_arxiv():
    """Execute RSS fetching task"""
    try:
        logger.info("Start fetching arXiv RSS")
        xml_str = get_arxiv_rss()
        logger.info("Successfully fetched arXiv RSS")
        return xml_str
    except Exception as e:
        logger.error(f"Failed to fetch RSS: {str(e)}")
        return False
        
def fetch_huggingface():
    """Execute Hugging Face fetching task"""
    try:
        logger.info("Start fetching Hugging Face RSS")
        xml_str = get_huggingface_papers()
        logger.info("Successfully fetched Hugging Face RSS")
        return xml_str
    except Exception as e:
        logger.error(f"Failed to fetch RSS: {str(e)}")
        return False

# HTTP 端点
@app.route('/status')
def get_status():
    """Get service status"""
    jobs = scheduler.get_jobs()
    next_run = jobs[0].next_run_time if jobs else None
    return jsonify({
        'status': 'running',
        'next_run': str(next_run) if next_run else None
    })

@app.route('/feed-arxiv', methods=['GET'])
def feed_arxiv():
    """Get paper list"""
    with open('feed/feed_arxiv.xml', 'r') as f:
        xml_str = f.read()
    return xml_str

@app.route('/feed-hf', methods=['GET'])
def feed_hf():
    """Get paper list"""
    with open('feed/feed_hf.xml', 'r') as f:
        xml_str = f.read()
    return xml_str

@app.route('/feed-arxiv-json', methods=['GET'])
def feed_arxiv_json():
    """Get paper list"""
    with open('feed/feed_arxiv.json', 'r') as f:
        json_str = f.read()
    return json_str

@app.route('/feed-hf-json', methods=['GET'])
def feed_hf_json():
    """Get paper list"""
    with open('feed/feed_hf.json', 'r') as f:
        json_str = f.read()
    return json_str

@app.route('/fetch-all', methods=['GET'])
def fetch_all():
    fetch_arxiv()
    fetch_huggingface()
    return "Success"

def init_scheduler():
    """Initialize scheduler"""
    scheduler.add_job(
        fetch_arxiv,
        trigger=CronTrigger(hour='*/6'),
        id='fetch_arxiv_job',
        name='Fetch arXiv RSS',
        max_instances=1,
        coalesce=True
    )
    scheduler.add_job(
        fetch_huggingface,
        trigger=CronTrigger(hour='*/6'),
        id='fetch_huggingface_job',
        name='Fetch Hugging Face Papers',
        max_instances=1,
        coalesce=True
    )
    scheduler.start()
    logger.info("Scheduler started")

if __name__ == '__main__':
    fetch_all()
    init_scheduler()
    app.run(host='0.0.0.0', port=5000)
