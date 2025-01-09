# Customized_paper_rss
## Feature
A customized AI papers rss feed for personal use.
### Filtering
User can filter the papers using api calls.
### Feeds
User can subscribe to the following feeds:
- arxiv-cs-AI
- hf
## Usage
```
pip install -r requirements.txt
```
Also we need to install Redis server on local machine. 
Port number is set to 6379 in `redis_client.py`.
Edit the `config.py` file to set the API key of the LLM. 
Using SiliconFlow Qwen-7b instruct API as default base url because it is free.
```
python server.py
```
Subscribe with the following url:
```
https://127.0.0.1:5000/feed-arxiv
```
```
https://127.0.0.1:5000/feed-hf
```
## Customization
User can customize the prompt for filtering and the number of papers to fetch by modifying the `config.py` file.

## TODO
- add more feeds
- add more source llm
