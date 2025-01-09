from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify
from get_arxiv import get_arxiv_rss
from logger_config import CustomLogger
from get_huggingface import get_huggingface_papers

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
    with open('feed_arxiv.xml', 'r') as f:
        xml_str = f.read()
    return xml_str

@app.route('/feed-hf', methods=['GET'])
def feed_hf():
    """Get paper list"""
    with open('feed_hf.xml', 'r') as f:
        xml_str = f.read()
    return xml_str

def init_scheduler():
    """Initialize scheduler"""
    scheduler.add_job(
        fetch_arxiv,
        trigger=CronTrigger(minute='*/1'),
        id='fetch_arxiv_job',
        name='Fetch arXiv RSS',
        max_instances=1,
        coalesce=True
    )
    scheduler.add_job(
        get_huggingface_papers,
        trigger=CronTrigger(minute='*/2'),
        id='fetch_huggingface_job',
        name='Fetch Hugging Face Papers',
        max_instances=1,
        coalesce=True
    )
    scheduler.start()
    logger.info("Scheduler started")

if __name__ == '__main__':
    init_scheduler()
    app.run(host='localhost', port=5000)
