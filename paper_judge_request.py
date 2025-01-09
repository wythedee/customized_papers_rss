import requests
import json
from logger_config import CustomLogger
from config import PROMPT, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

class PaperJudgeRequest:
    def __init__(self, model=LLM_MODEL):
        self.model = model
        self.url = LLM_BASE_URL
        self.logger = CustomLogger()

    def send_paper_judge_request(self, paper):
        self.logger.info(f"Sending paper judge request for model: {self.model}")
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT
                    + paper 
                    + "Template: {\"explanation\": \"<explanation>\", \"answer\": <yes/no>, \"summary\": \"<summary>\"}"
                    + "Note that you must answer in json format. Answer:"
                }
            ],
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.url, json=payload, headers=headers)
        self.logger.info(f"Received response with status code: {response.status_code}")

        try:
            content = json.loads(response.text.replace("```json", "").replace("```", ""))["choices"][0]["message"]["content"]
        except Exception as e:
            self.logger.error(f"Failed to parse response JSON: {e}")
            self.logger.error(f"Received response content: {response.text}")
            return None, None

        try:
            answer = json.loads(content)
            self.logger.debug("Successfully parsed response JSON")
        except Exception as e:
            self.logger.error(f"Failed to parse response JSON: {e}")
            return None, None

        return answer["answer"], answer["explanation"], answer["summary"]
    
if __name__ == "__main__":
    pjr = PaperJudgeRequest()
    answer = pjr.send_paper_judge_request("The paper presents a unified dataset for document QA, reformulating Document AI tasks into QA tasks and releasing OCR and bounding box information, to evaluate the impact of different prompting techniques on large language models. arXiv:2501.03403v1 Announce Type: cross Abstract: We present a unified dataset for document Question-Answering (QA), which is obtained combining several public datasets related to Document AI and visually rich document understanding (VRDU). Our main contribution is twofold: on the one hand we reformulate existing Document AI tasks, such as Information Extraction (IE), into a Question-Answering task, making it a suitable resource for training and evaluating Large Language Models; on the other hand, we release the OCR of all the documents and include the exact position of the answer to be found in the document image as a bounding box. Using this dataset, we explore the impact of different prompting techniques (that might include bounding box information) on the performance of open-weight models, identifying the most effective approaches for document comprehension.")
    print(answer)