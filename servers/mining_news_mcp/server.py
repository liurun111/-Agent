"""mining-news-mcp — 矿业新闻搜索 MCP Server (FastMCP + SSE transport)"""
import sys, os, json, logging

from mcp.server.fastmcp import FastMCP

# 在导入 mock 之前配置路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mining-news-mcp")


def register_tools(mcp: FastMCP):
    from mock_data import NEWS, FULL_TEXT
    from datetime import date, timedelta

    def _days_ago(n: int) -> str:
        return str(date.today() - timedelta(days=n))

    @mcp.tool()
    def search(query: str, days: int = 7) -> str:
        """搜索矿业新闻。按关键词和时间范围搜索，返回匹配的新闻列表。

        Args:
            query: 搜索关键词，例如 "Pilbara lithium" 或 "锂矿出口政策"
            days: 搜索最近多少天，默认7天
        """
        cutoff = _days_ago(days)
        keywords = query.lower().split()
        results = []
        for item in NEWS:
            text = f"{item['title']} {item['summary']}".lower()
            if item["date"] >= cutoff and any(kw in text for kw in keywords):
                results.append(item)
        logger.info(f"search(query='{query}', days={days}) -> {len(results)} results")
        return json.dumps(results, ensure_ascii=False, indent=2)

    @mcp.tool()
    def fetch_article(url: str) -> str:
        """获取新闻全文。

        Args:
            url: 新闻URL，从 search() 返回结果中获取
        """
        text = FULL_TEXT.get(url)
        if text is None:
            for item in NEWS:
                if item["url"] == url:
                    text = f"{item['title']}\n\n{item['summary']}\n\n[Full text not available in mock data]"
                    break
            if text is None:
                text = "[Article not found]"
        result = {"url": url, "full_text": text}
        logger.info(f"fetch_article(url='{url}') -> {len(text)} chars")
        return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "sse")
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8001"))

    mcp = FastMCP("mining-news-mcp", host=host, port=port)
    register_tools(mcp)

    if transport == "sse":
        logger.info(f"Mining News MCP Server -> SSE transport on {host}:{port}")
        mcp.run(transport="sse")
    else:
        logger.info("Mining News MCP Server -> stdio transport")
        mcp.run(transport="stdio")
