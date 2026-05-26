import os
from email import message

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
"""
调用方式
1.直接用init_chat_model
2.用所属大模型的 例如 chatOpenAI
"""

from langchain.chat_models import init_chat_model

# llm = init_chat_model(model='gpt-4o-mini', api_key=os.getenv("OPENAI_API_KEY"),
#                         base_url=os.getenv("OPENAI_BASE_URL"))
llm = ChatOpenAI(model='gpt-4o-mini', api_key=api_key,
                       base_url=base_url)
response = llm.invoke("怎么哄女朋友")

print(response.content)