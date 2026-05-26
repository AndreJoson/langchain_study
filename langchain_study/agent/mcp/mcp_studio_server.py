#创建mcp
from mcp.server import FastMCP

mcp = FastMCP("demo")


@mcp.tool()
def add(a:int,b:int)->int:
    return a+b

@mcp.resource("greeting://default")
def get_greeting()->str:
    return "Hello World"


@mcp.prompt()
def greet_user(name:str,style:str = "friendly")->str:
     styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
     }
     return f"为{name}{styles.get(style, styles['friendly'])}"
