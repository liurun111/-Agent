# MCP 矿权日报 Agent — 5 分钟启动指南

## 前置条件

- 安装 Docker Desktop
- 申请 LLM API Key（DeepSeek / OpenAI / Claude 均可）

## 快速启动（Docker）

```bash
# 设置 API Key (Linux/Mac)
export OPENAI_API_KEY=sk-your-key
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export LLM_MODEL=deepseek-chat

# 启动 + 运行
docker-compose up -d
docker-compose run agent python agent/react_agent.py
```

CMD:
```cmd
set OPENAI_API_KEY=sk-your-key
set OPENAI_BASE_URL=https://api.deepseek.com/v1
set LLM_MODEL=deepseek-chat
docker-compose up -d
docker-compose run agent python agent/react_agent.py
```

输出 Markdown 矿权日报 → 终端打印 + 保存 `report.md`。

## 本地开发（不用 Docker，开 4 个终端）

> 以下命令需在项目根目录执行。先进项目目录：`cd 题2`

**CMD:**
```cmd
:: 终端1 — mining-news-mcp (端口 8001)
set MCP_TRANSPORT=sse
set MCP_HOST=0.0.0.0
set MCP_PORT=8001
python servers/mining_news_mcp/server.py

:: 终端2 — mineral-pdf-mcp (端口 8002)
set MCP_TRANSPORT=sse
set MCP_HOST=0.0.0.0
set MCP_PORT=8002
python servers/mineral_pdf_mcp/server.py

:: 终端3 — lme-price-mcp (端口 8003)
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

**PowerShell:**
```powershell
# 终端1 — mining-news-mcp (端口 8001)
$env:MCP_TRANSPORT="sse"
$env:MCP_HOST="0.0.0.0"
$env:MCP_PORT="8001"
python servers/mining_news_mcp/server.py

# 终端2 — mineral-pdf-mcp (端口 8002)
$env:MCP_TRANSPORT="sse"
$env:MCP_HOST="0.0.0.0"
$env:MCP_PORT="8002"
python servers/mineral_pdf_mcp/server.py

# 终端3 — lme-price-mcp (端口 8003)
$env:MCP_TRANSPORT="sse"
$env:MCP_HOST="0.0.0.0"
$env:MCP_PORT="8003"
python servers/lme_price_mcp/server.py

# 终端4 — Agent
$env:OPENAI_API_KEY="sk-your-key"
$env:OPENAI_BASE_URL="https://api.deepseek.com/v1"
$env:LLM_MODEL="deepseek-chat"
python agent/react_agent.py
```

## 接入 Claude Desktop / Cursor

将项目目录下的 `mcp-config.json` 复制到对应配置文件：

- **Claude Desktop** → `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor** → `.cursor/mcp.json`

重启即可在对话中直接使用 3 个 MCP server。

## 架构

```
用户 "生成Pilbara锂矿今日简报"
  │
  ▼
agent (ReAct + LLM)
  │
  ├── MCP SSE ── mining-news-mcp  :8001
  │   ├── search(query, days)        → 新闻搜索
  │   └── fetch_article(url)         → 全文获取
  │
  ├── MCP SSE ── mineral-pdf-mcp  :8002
  │   └── extract_resources(pdf_url) → NI 43-101 储量抽取 (PDF解析)
  │
  └── MCP SSE ── lme-price-mcp    :8003
      ├── get_price(commodity, date)  → 单日价格
      └── get_trend(commodity, days)  → 价格走势

  ▼
Markdown 日报
  一、新闻摘要
  二、NI 43-101 储量数据
  三、价格走势
  四、风险提示
  五、数据来源
```

## 停用

```bash
docker-compose down
```
