"""ReAct Agent — 矿权日报生成器
通过 MCP SSE 协议连接 3 个 server，LLM 编排工具调用，生成 Markdown 简报
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, logging, asyncio

from openai import OpenAI

from agent.config import LLM_CONFIG, MCP_SERVERS, TOOLS
from agent.prompt import get_system_prompt

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("react-agent")


# ═══ MCP Client (官方 SDK SSE) ═══
class MCPClient:
    """用官方 mcp SDK 通过 SSE 调用工具"""

    def __init__(self, servers: dict):
        self.servers = servers

    def call(self, tool_name: str, arguments: dict) -> str:
        server_id = _route_tool(tool_name)
        server = self.servers.get(server_id)
        if not server:
            return json.dumps({"error": f"No MCP server for tool '{tool_name}'"})

        full_name = {
            "search_news": "search",
            "fetch_article": "fetch_article",
            "extract_resources": "extract_resources",
            "get_price": "get_price",
            "get_trend": "get_trend",
        }.get(tool_name, tool_name)

        return asyncio.run(self._call_async(server["url"], full_name, arguments))

    async def _call_async(self, url: str, tool_name: str, args: dict) -> str:
        from mcp.client.session import ClientSession
        from mcp.client.sse import sse_client

        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, args)
                if result.content:
                    return result.content[0].text
                return str(result)


def _route_tool(tool_name: str) -> str:
    return {
        "search_news": "mining-news",
        "fetch_article": "mining-news",
        "extract_resources": "mineral-pdf",
        "get_price": "lme-price",
        "get_trend": "lme-price",
    }.get(tool_name, "mining-news")


# ═══ ReAct Loop ═══
class ReactAgent:
    def __init__(self):
        self.llm = OpenAI(api_key=LLM_CONFIG["api_key"], base_url=LLM_CONFIG["base_url"])
        self.mcp = MCPClient(MCP_SERVERS)
        self.model = LLM_CONFIG["model"]
        self.temperature = LLM_CONFIG["temperature"]
        self.max_tokens = LLM_CONFIG["max_tokens"]

    def run(self, user_query: str) -> str:
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_query},
        ]

        for i in range(12):
            logger.info(f"--- ReAct iteration {i + 1} ---")

            response = self.llm.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            msg = response.choices[0].message

            if not msg.tool_calls:
                logger.info("No tool calls -> final answer")
                return msg.content or ""

            # 记录 assistant 消息（含 tool_calls）
            messages.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in msg.tool_calls
                ]
            })

            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)
                logger.info(f"  Tool: {fn_name}({json.dumps(fn_args, ensure_ascii=False)})")

                try:
                    result = self.mcp.call(fn_name, fn_args)
                except Exception as e:
                    result = json.dumps({"error": str(e)})
                    logger.error(f"  MCP call failed: {e}")

                if len(result) > 4000:
                    result = result[:4000] + "\n...[truncated]"

                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
                logger.info(f"  Result: {len(result)} chars")

        logger.warning("Max iterations, forcing final")
        return self._force_final(messages)

    def _force_final(self, messages: list) -> str:
        messages.append({"role": "user", "content": "请基于以上所有数据，生成最终的矿权日报 Markdown。不要再调用工具。"})
        response = self.llm.chat.completions.create(
            model=self.model, messages=messages,
            temperature=self.temperature, max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content or ""


# ═══ Entry Point ═══
def main():
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "生成一份关于Pilbara锂矿的今日简报"

    agent = ReactAgent()
    logger.info(f"Query: {user_query}")

    markdown = agent.run(user_query)

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print(markdown)
    print(f"\n--- report.md ---")


if __name__ == "__main__":
    main()
