# 矿权日报 Agent

基于 MCP (Model Context Protocol) 的矿业情报日报系统。3 个独立 MCP server + ReAct Agent，输入自然语言 → 输出 Markdown 矿权日报。

## 架构

```
用户 "生成Pilbara锂矿今日简报"
  │
  ▼
agent (ReAct + LLM)
  │
  ├── MCP SSE ─ mining-news-mcp  :8001 ─ search / fetch_article
  ├── MCP SSE ─ mineral-pdf-mcp  :8002 ─ extract_resources (NI 43-101 PDF解析)
  └── MCP SSE ─ lme-price-mcp    :8003 ─ get_price / get_trend
  │
  ▼
Markdown 日报
  一、近期新闻摘要
  二、NI 43-101 资源储量
  三、价格走势（近30日）
  四、风险提示
  五、数据来源
```

## 快速启动

```cmd
:: 安装依赖
pip install -r requirements.txt -i https://pypi.org/simple/

:: 终端1 — mining-news-mcp
set MCP_TRANSPORT=sse
set MCP_HOST=0.0.0.0
set MCP_PORT=8001
python servers/mining_news_mcp/server.py

:: 终端2 — mineral-pdf-mcp
set MCP_TRANSPORT=sse
set MCP_HOST=0.0.0.0
set MCP_PORT=8002
python servers/mineral_pdf_mcp/server.py

:: 终端3 — lme-price-mcp
set MCP_TRANSPORT=sse
set MCP_HOST=0.0.0.0
set MCP_PORT=8003
python servers/lme_price_mcp/server.py

:: 终端4 — Agent
set OPENAI_API_KEY=sk-your-key
set OPENAI_BASE_URL=https://api.deepseek.com/v1
set LLM_MODEL=deepseek-chat
python agent/react_agent.py
```

## Docker

```cmd
set OPENAI_API_KEY=sk-your-key
set OPENAI_BASE_URL=https://api.deepseek.com/v1
set LLM_MODEL=deepseek-chat
docker-compose up -d
docker-compose run agent python agent/react_agent.py
```

## 项目结构

```
├── servers/
│   ├── mining_news_mcp/   # 新闻搜索
│   ├── mineral_pdf_mcp/   # NI 43-101 PDF 解析
│   └── lme_price_mcp/     # 金属价格
├── agent/                 # ReAct Agent + LLM 编排
├── shared/                # 共享数据模型
├── docker-compose.yml
├── mcp-config.json        # Claude Desktop / Cursor 集成
└── RUN.md                 # 详细启动指南
```

## 接入 Claude Desktop

将 `mcp-config.json` 复制到 `%APPDATA%\Claude\claude_desktop_config.json` 重启即可。
