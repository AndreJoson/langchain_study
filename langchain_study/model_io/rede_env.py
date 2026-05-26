import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

print(f"api地址: {api_key}, base_url: {base_url}")
