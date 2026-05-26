from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_study.model_io.lc_static_class import LS

template = PromptTemplate(template="讲一个关于{topic}的笑话", input_variables=["topic"])

client = ChatOpenAI(model=LS.get_static_model(),base_url=LS.get_base_url(),api_key=LS.get_api_key())

par = StrOutputParser()

chain = template | client | par

invoke = chain.invoke({"topic": "人工智能"})

print(invoke)
