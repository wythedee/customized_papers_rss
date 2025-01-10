# Customized_paper_rss
## Feature
A customized AI papers rss feed for personal use.
### Filtering
User can filter the papers related to the field of interest using api calls.
### Summarization
Summarization of each paper and explanation why the paper is selected are provided in the feed.
### Feeds
User can subscribe to the following feeds:
- arxiv-cs-AI
- hf
## Usage
```
pip install -r requirements.txt
```
Also we need to install [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) on our local machine. 
Port number is set to 6379 in `redis_client.py`.
Edit the `config.py` file to set the API key of the LLM. 
Using SiliconFlow Qwen-7b instruct API as default base url because it is free.
```
python server.py
```
### Subscription
Subscribe with the following url:
Arxiv:
```
https://127.0.0.1:5000/feed-arxiv # xml
https://127.0.0.1:5000/feed-arxiv-json # json
```
Hugging Face:
```
https://127.0.0.1:5000/feed-hf # xml
https://127.0.0.1:5000/feed-hf-json # json
```
### Customization
User can customize base rss url, the field of interest, language for answering, prompt for filtering and the number of papers to fetch by modifying the `config.py` file.

## TODO
- add more feeds support
- add more source llm support
