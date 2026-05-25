import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from model_io.lc_static_class import LS

load_dotenv()
# 异步调用
# async def langchain_invoke():
#     chatOpenAI = ChatOpenAI(model=LS.get_static_model(),
#                             api_key=LS.get_api_key(),
#                             base_url=LS.get_base_url())
#     message  = [{"role":"user","content":"你是谁"},{"role":"system","content":"你是一个数学家"}]
#
#     res = await chatOpenAI.ainvoke(message)
#
#     print(res.content)


#流式调用
# chatOpenAI = ChatOpenAI(model=LS.get_static_model(),
#                         api_key=LS.get_api_key(),
#                         base_url=LS.get_base_url())
# message  = [{"role":"user","content":"什么是LangChain"},{"role":"system","content":"你是一个agent工程师"}]
# res = chatOpenAI.stream(message)
#
# for r in res:
#     print(r.content)

#批量调用
chatOpenAI = ChatOpenAI(model=LS.get_static_model(),
                        api_key=LS.get_api_key(),
                        base_url=LS.get_base_url())
message  = [[{"role":"user","content":"什么是LangChain"},{"role":"system","content":"你是一个agent工程师"}],
            [{"role":"user","content":"为什么1+1=2"},{"role":"system","content":"你是一个数学工程师"}]]

res = chatOpenAI.batch(message)

for r in res:
    print(r.content)

