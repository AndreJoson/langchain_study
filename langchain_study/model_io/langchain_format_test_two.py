from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
load_dotenv()
from langchain_study.model_io.lc_static_class import LS

ai = ChatOpenAI(model=LS.get_static_model())

class FormatModel(BaseModel):
    name: list[str]
    description: list[str]


output = ai.with_structured_output(FormatModel)

res = output.invoke([("user", "统计下今年节日")])
print(res)
