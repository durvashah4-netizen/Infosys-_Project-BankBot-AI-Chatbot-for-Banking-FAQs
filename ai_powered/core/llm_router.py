import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from core.prompt_templates import SYSTEM_PROMPT, USER_PROMPT

load_dotenv()

class LLMRouter:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def invoke(self, msg: str) -> dict:
        prompt = SYSTEM_PROMPT + USER_PROMPT.format(message=msg)
        res = self.llm.invoke(prompt)
        return json.loads(res.content)
