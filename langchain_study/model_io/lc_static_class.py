import os

from dotenv import load_dotenv

load_dotenv()

class LS():
    @staticmethod
    def get_api_key():
        return os.getenv("OPENAI_API_KEY")

    @staticmethod
    def get_base_url():
        return os.getenv("OPENAI_BASE_URL")

    @staticmethod
    def get_static_model():
        return "gpt-4o-mini"

    @staticmethod
    def getUri():
        return "http://localhost:19530"
