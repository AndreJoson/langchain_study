from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()
from model_io.lc_static_class import LS

ai = ChatOpenAI(model=LS.get_static_model())


class FormatModel(BaseModel):
    name: str = Field(description="名字")
    description: str= Field(description="描述")


parser = JsonOutputParser(pydantic_object=FormatModel)

message = [("system",parser.get_format_instructions()),("user","总结一年中比较重要的节日")]
res = ai.invoke(message)

print(parser.parse(res.content))
