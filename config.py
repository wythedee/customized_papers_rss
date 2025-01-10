YOUR_FIELD = ""
LANGUAGE = "English"
PROMPT = f"Please read the following abstract of a paper and evaluate if the research \
        could be adapted to or is related to the field of {YOUR_FIELD}. \
        Provide a short explanation for your reasoning. Also a sentence of summarization for the paper, including \
        the motivation, the key methods, contributions, and the results. Abstract: " 

PAPER_NUMBER = 50

PAPER_EXPIRE_TIME = 172800

# LLM
LLM_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
LLM_API_KEY = ""
LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"