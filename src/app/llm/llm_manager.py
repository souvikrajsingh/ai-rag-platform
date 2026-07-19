from langchain_google_genai import ChatGoogleGenerativeAI
from src.app.config.settings import Settings

settings = Settings();

class LLMManager:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0
        )
    def generate(self,prompt:str) -> str:
        response = self.llm.invoke(prompt)
        return response.text