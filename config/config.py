# Customize
YOUR_FIELD = "multimodal misinformation detection"
FIELD_DESCRIPTION = "This research field focus on image-text out-of-context misinformation detection. \
        This kind of misinformation is formed with wrongly matched image and text. \
        So you nedd to focus more on the alignment between image and text or other modalities and reasoning for the ability of finding the mismatched part. \
        Also please pay attention to 'causal inference' related papers. \
        Multimodal or LLM related papers should be considered, too"
LANGUAGE = "Chinese"
PROMPT = f"Please read the following abstract of a paper and evaluate if the research \
        could be adapted to or is somehow related to the field of {YOUR_FIELD}. \
        {FIELD_DESCRIPTION} \
        Provide a short explanation for your reasoning. Also a sentence of summarization for the paper, including \
        the motivation, the key methods, contributions, and the results. Abstract: " 

PAPER_NUMBER = 20

# LLM
LLM_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
LLM_API_KEY = ""
LLM_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

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
