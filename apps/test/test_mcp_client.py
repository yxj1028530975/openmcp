import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()


async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8000/mcp") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            # result = await session.call_tool("add", arguments={"num_1": 2, "num_2": 3})
            # print(f"2 + 3 = {result.content[0].text}")

            result = await session.call_tool("get_hot_list", arguments={"platform": "weibo"})
            print(f"微博热榜: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())