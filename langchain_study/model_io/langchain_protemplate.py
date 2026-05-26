from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
from langchain_study.model_io.lc_static_class import LS

#提示词模版
prompt_template = ChatPromptTemplate.from_messages(
    messages=[("system", "你是一个专业的评论员"), ("user", "请评价{product}的优缺点，包括{aspect1}和{aspect2}")])


messages = prompt_template.invoke({"product": "iPhone 15", "aspect1": "性能", "aspect2": "外观"})

client = ChatOpenAI(model=LS.get_static_model(),base_url=LS.get_base_url(),api_key=LS.get_api_key())

invoke = client.invoke(messages)

print(invoke.content)

