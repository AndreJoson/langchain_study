import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# 创建连接
client = OpenAI()

chat = client.chat.completions.create(model='gpt-4o-mini',
                                      messages=[{"role": "user", "content": "将'你好'翻译成意大利语"}])
#chat2 = client.responses.create(model='gpt-4o-mini', input="你好")

#print(chat2)

print(chat)
