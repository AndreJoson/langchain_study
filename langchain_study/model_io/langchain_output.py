from typing import List

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import Field, BaseModel

from langchain_study.model_io.lc_static_class import LS

#输出约束，一种提示词模版约束，一种厂商提供的
load_dotenv()

chatOpenAI = ChatOpenAI(model=LS.get_static_model(),base_url=LS.get_base_url(),api_key=LS.get_api_key())


class Prime(BaseModel):
    prime:List[int]=Field(description="素数")
    count:List[int] = Field(description="小于该素数的素数个数")

#提示词来解决 输出格式问题
json_parser = JsonOutputParser(pydantic_object=Prime)

message = [
    {"role": "system", "content": json_parser.get_format_instructions()},
    {"role": "user", "content": "任意生成5个1000-100000之间素数，并标出小于该素数的素数个数"}
]
result = chatOpenAI.invoke(message)

#厂商自带的
output = chatOpenAI.with_structured_output(schema=Prime)
output_invoke = output.invoke("任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")

print(output_invoke)
print(result.content)

parser_invoke = json_parser.invoke(result)

print(type(parser_invoke))
