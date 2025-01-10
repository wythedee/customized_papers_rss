# Customize
YOUR_FIELD = ""
LANGUAGE = "English"
PROMPT = f"Please read the following abstract of a paper and evaluate if the research \
        could be adapted to or is related to the field of {YOUR_FIELD}. \
        Provide a short explanation for your reasoning. Also a sentence of summarization for the paper, including \
        the motivation, the key methods, contributions, and the results. Abstract: " 

PAPER_NUMBER = 40

# LLM
LLM_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
LLM_API_KEY = ""
LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

# RSS
RSS_URL = "http://rss.arxiv.org/rss/cs.AI"

# Hugging Face
HUGGINFACE_URL = "https://huggingface.co/papers"

# Redis
REDIS_DB_ARXIV = 0
REDIS_DB_HUGGINFACE = 1
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

PAPER_EXPIRE_TIME = 172800