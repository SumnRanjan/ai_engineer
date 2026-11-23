"""Minimal MCP client: connects to server.py over stdio, discovers and calls its capabilities.

Run:  python client.py
"""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Use the same Python (venv) as the client, and find server.py next to this file
SERVER = Path(__file__).parent / "server.py"
server_params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # handshake

            # 1. Discovery
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            prompts = await session.list_prompts()
            print("Prompts:", [p.name for p in prompts.prompts])

            # 2. Call tools (in a real agent, the LLM picks these)
            result = await session.call_tool("add", {"a": 2, "b": 3})
            print("add(2, 3) =", result.content[0].text)

            result = await session.call_tool("get_order_status", {"order_id": "4521"})
            print(result.content[0].text)

            # 3. Read a resource
            res = await session.read_resource("orders://4522")
            print("Resource:", res.contents[0].text)

            # 4. Get a prompt
            prompt = await session.get_prompt("summarize_order", {"order_id": "4521"})
            print("Prompt:", prompt.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())