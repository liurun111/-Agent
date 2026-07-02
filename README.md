# 矿权日报 Agent

基于 **MCP (Model Context Protocol)** 协议搭建的矿业情报自动化系统。3 个独立 MCP Server 提供新闻、储量、价格数据，1 个 ReAct Agent 调用 LLM 编排生成 Markdown 矿权日报。

## 项目背景

矿业投资决策依赖三类数据：**新闻事件**（政策、并购、投产）、**资源储量**（NI 43-101 技术报告）、**金属价格**（LME/SHFE 行情）。本项目用 MCP 协议解耦数据源，Agent 按需调用，LLM 汇总生成结构化日报。

## 三个 MCP Server

### 1. mining-news-mcp（端口 8001）

提供矿业新闻的语义搜索和全文获取。

| 工具 | 参数 | 功能 |
|------|------|------|
| `search` | `query`, `days` | 按关键词 + 时间范围搜索新闻，返回标题、摘要、来源、日期、URL |
| `fetch_article` | `url` | 根据 URL 获取新闻全文 |

内置 28 条 Pilbara 锂矿相关中英文新闻（覆盖近 30 天），来源包括 mining.com、Reuters、ABC News、S&P Global、Benchmark Mineral Intelligence、中国稀土集团官网等。

### 2. mineral-pdf-mcp（端口 8002）

从 NI 43-101 技术报告 PDF 中提取 Indicated 和 Inferred 资源量。

| 工具 | 参数 | 功能 |
|------|------|------|
| `extract_resources` | `pdf_url` | 解析 PDF，返回矿石量(Mt)、品位(g/t 或 %)、金属量(oz 或 t) |

支持两层解析策略：`pypdf` 提取文本 + 正则匹配（兜底），`pdfplumber` 提取表格（可选增强）。传 `list` 可列出内置的 3 份报告（Pilgangoora / Boddington / Hemlo）。

### 3. lme-price-mcp（端口 8003）

提供金属期货价格的单日查询和趋势分析。

| 工具 | 参数 | 功能 |
|------|------|------|
| `get_price` | `commodity`, `date` | 查询指定商品在指定日期的收盘价 |
| `get_trend` | `commodity`, `days` | 返回近 N 天价格序列，含涨跌幅、最高最低 |

支持 6 个品种：碳酸锂、氢氧化锂、铜、锌、镍、62%铁矿石。内置 31 天价格序列（基于真实价格区间模拟）。

## Agent

自写 ReAct (Reasoning + Acting) 循环，核心流程：

```
用户输入
  ↓
LLM 解析意图 → 拆解子任务
  ↓
Thought: 需要搜索 Pilbara 锂矿新闻
  Action: call mining-news-mcp.search("Pilbara lithium", days=7)
  Observation: 5 条新闻
  ↓
Thought: 需要 NI 43-101 储量数据
  Action: call mineral-pdf-mcp.extract_resources("pilgangoora")
  Observation: Indicated 413.9Mt + Inferred 95.1Mt
  ↓
Thought: 需要锂价走势
  Action: call lme-price-mcp.get_trend("lithium_carbonate", days=30)
  Observation: 涨 +6.6%，最高 ¥134,101，最低 ¥121,365
  ↓
Thought: 数据齐全，生成简报
  → Markdown 日报（新闻摘要 + 储量表 + 价格走势 + 风险提示 + 数据来源）
```

LLM 通过 OpenAI 兼容接口调用，支持 DeepSeek / GPT-4o / Claude。

## 技术选型

| 层面 | 选择 | 说明 |
|------|------|------|
| MCP 框架 | FastMCP (Python `mcp`) | `@mcp.tool()` 装饰器定义工具，自动生成 JSON-RPC 接口 |
| Agent 模式 | 自写 ReAct | 6 个工具无需 LangGraph 状态图，循环足够 |
| LLM 调用 | `openai` SDK | 兼容 `base_url`，切换模型只需改环境变量 |
| PDF 解析 | pypdf + pdfplumber + 正则 | 三层兜底，缺少 pdfplumber 也能跑 |
| Transport | SSE (HTTP) | Docker 容器间通信；本地开发 stdio 也可 |
| 部署 | docker-compose | 4 容器（3 server + 1 agent），healthcheck 保障启动顺序 |

## 项目结构

```
题2/
├── README.md                           # 项目说明
├── RUN.md                              # 详细启动指南
├── requirements.txt                    # Python 依赖
├── docker-compose.yml                  # 4 容器编排
├── mcp-config.json                     # Claude Desktop / Cursor 集成配置
├── shared/
│   └── schemas.py                      # Pydantic 数据模型（NewsItem, ResourceReport, PricePoint）
├── servers/
│   ├── mining_news_mcp/
│   │   ├── Dockerfile
│   │   ├── server.py                   # FastMCP Server
│   │   └── mock_data.py               # 28 条新闻 + 4 篇全文
│   ├── mineral_pdf_mcp/
│   │   ├── Dockerfile
│   │   ├── server.py                   # FastMCP Server + pypdf 解析
│   │   └── mock_ni43_101.py           # 3 份 NI 43-101 储量
│   └── lme_price_mcp/
│       ├── Dockerfile
│       ├── server.py                   # FastMCP Server
│       └── mock_prices.py             # 6 品种价格序列
└── agent/
    ├── Dockerfile
    ├── config.py                       # LLM 配置 + MCP 端点 + Tool 定义
    ├── prompt.py                       # System Prompt
    ├── react_agent.py                  # ReAct 主循环 + MCP SSE 客户端
    └── report_builder.py              # 简报模板 + 风险推理
```

## 运行

```cmd
pip install -r requirements.txt -i https://pypi.org/simple/

:: 3 个终端启动 MCP Server
set MCP_TRANSPORT=sse & set MCP_HOST=0.0.0.0 & set MCP_PORT=8001
python servers/mining_news_mcp/server.py

set MCP_TRANSPORT=sse & set MCP_HOST=0.0.0.0 & set MCP_PORT=8002
python servers/mineral_pdf_mcp/server.py

set MCP_TRANSPORT=sse & set MCP_HOST=0.0.0.0 & set MCP_PORT=8003
python servers/lme_price_mcp/server.py

:: Agent
set OPENAI_API_KEY=sk-xxx & set OPENAI_BASE_URL=https://api.deepseek.com/v1 & set LLM_MODEL=deepseek-chat
python agent/react_agent.py
```

输出保存为 `report.md`。

## Docker

```cmd
set OPENAI_API_KEY=sk-xxx
docker-compose up -d
docker-compose run agent python agent/react_agent.py
```
