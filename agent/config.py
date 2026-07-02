"""Agent 配置 — LLM provider + MCP 连接端点"""
import os


# ═══ LLM 配置 ═══
# 通过环境变量切换，默认使用 OpenAI 兼容接口
LLM_CONFIG = {
    "api_key": os.environ.get("OPENAI_API_KEY", "sk-placeholder"),
    "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "model": os.environ.get("LLM_MODEL", "gpt-4o"),
    "temperature": float(os.environ.get("LLM_TEMPERATURE", "0.3")),
    "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "4096")),
}


# ═══ MCP Server 端点 ═══
# Docker 环境通过服务名访问（每容器独立hostname），本地开发通过 localhost
MCP_SERVERS = {
    "mining-news": {
        "name": "mining-news-mcp",
        "url": f"http://{os.environ.get('NEWS_MCP_HOST', 'localhost')}:8001/sse",
    },
    "mineral-pdf": {
        "name": "mineral-pdf-mcp",
        "url": f"http://{os.environ.get('PDF_MCP_HOST', 'localhost')}:8002/sse",
    },
    "lme-price": {
        "name": "lme-price-mcp",
        "url": f"http://{os.environ.get('PRICE_MCP_HOST', 'localhost')}:8003/sse",
    },
}


# ═══ 工具函数定义 (传给 LLM function calling) ═══
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "搜索矿业新闻。按关键词和时间范围搜索，返回匹配的新闻列表。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "days": {"type": "integer", "description": "搜索最近多少天，默认7"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_article",
            "description": "获取新闻全文。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "新闻URL"},
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_resources",
            "description": "从NI 43-101矿权报告PDF中提取Indicated和Inferred Resources储量数据。传'list'列出所有可用报告。",
            "parameters": {
                "type": "object",
                "properties": {
                    "pdf_url": {"type": "string", "description": "NI 43-101报告的URL，或传'list'查看可用报告"},
                },
                "required": ["pdf_url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "查询指定商品在指定日期的收盘价。支持: lithium_carbonate, lithium_hydroxide, copper, zinc, nickel, iron_ore_62",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {"type": "string", "description": "商品名称"},
                    "date": {"type": "string", "description": "日期 YYYY-MM-DD"},
                },
                "required": ["commodity", "date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_trend",
            "description": "查询指定商品近N天的价格走势，返回序列及涨跌统计。支持: lithium_carbonate, lithium_hydroxide, copper, zinc, nickel, iron_ore_62",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {"type": "string", "description": "商品名称"},
                    "days": {"type": "integer", "description": "查询天数，默认30"},
                },
                "required": ["commodity"],
            },
        },
    },
]
