from mcp import StdioServerParameters


async def stdio_run():
    StdioServerParameters(
        command=r"/Users/wangbowei/PycharmProjects/langchain_study/.venv/Scripts/python.exe",
        args=[r"./mcp_studio_server.py"]
    )