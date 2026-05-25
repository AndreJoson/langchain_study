from langchain_ollama import ChatOllama

#本地大模型调用
ollama = ChatOllama(model="qwen3:8b", base_url="http://localhost:11434")

messages = [{"role": "user", "content": "你好，请介绍一下你自己"}]

res = ollama.invoke(messages)

print(res.content)
