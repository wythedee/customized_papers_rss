# Customize
YOUR_FIELD = "multimodal misinformation detection"
FIELD_DESCRIPTION = (
    "This research field focuses on detecting image-text out-of-context misinformation, "
    "where misinformation arises from mismatched images and text. "
    "Emphasis should be placed on analyzing alignment between image, text, or other modalities, "
    "and reasoning to identify discrepancies. "
    "Additionally, consider papers related to 'causal inference,' "
    "as well as those involving multimodal approaches or large language models (LLMs)."
)

LANGUAGE = "Chinese"

PROMPT = (
    f"Please evaluate whether the following paper abstract aligns with "
    f"or could be adapted to the field of {YOUR_FIELD}. "
    f"{FIELD_DESCRIPTION} "
    f"However, also include it in my customized reading list if it offers valuable insights, "
    f"learning opportunities, or practical help, even if it’s not directly related to {YOUR_FIELD}. "
    f"Provide a concise explanation, including how its ideas could benefit my research or skills in {YOUR_FIELD}. "
    f"Additionally, summarize the paper in one sentence, covering its motivation, "
    f"key methods, contributions, and results. "
    f"Abstract: "
)

PAPER_NUMBER = 10

# LLM
LLM_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
LLM_API_KEY = "sk-yyexckoribsghgszghxqrejfjsotcxfwkcjpwgngocyrngcg"
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
