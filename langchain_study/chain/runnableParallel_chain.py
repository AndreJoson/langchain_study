from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel

from langchain_study.model_io.lc_static_class import LS

client = init_chat_model(model=LS.get_static_model(), base_url=LS.get_base_url(), api_key=LS.get_api_key())

english_chain = (PromptTemplate.from_template(template="把这个句子{topic}翻译成英文") | client | StrOutputParser())
korea_chain = (PromptTemplate.from_template(template= "把这个句子{topic}翻译成韩文") | client | StrOutputParser())

map_chain = RunnableParallel(english=english_chain, korean=korea_chain)
result = map_chain.invoke({"topic": "我是人工智能"})

print(result)
