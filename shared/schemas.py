"""共享 Pydantic 数据模型 — 所有 MCP server + agent 共用"""
from pydantic import BaseModel


# ═══ 新闻 ═══
class NewsItem(BaseModel):
    title: str
    summary: str
    source: str          # 来源：mining.com / Reuters / 中国稀土集团
    date: str            # "2026-06-28"
    url: str

class Article(BaseModel):
    title: str
    full_text: str
    source: str
    date: str
    url: str


# ═══ 储量 (NI 43-101) ═══
class ResourceRow(BaseModel):
    category: str        # "Indicated" | "Inferred"
    ore_tonnes_mt: float
    grade: str           # "1.15% Li2O" | "1.2 g/t Au"
    metal_content: str   # "1.09 Mt Li2O" | "3.2 Moz Au"

class ResourceReport(BaseModel):
    project: str         # "Pilgangoora" | "Boddington" | "Hemlo"
    owner: str           # "Pilbara Minerals" | "Newmont" | "Barrick"
    report_date: str     # NI 43-101 报告日期
    pdf_url: str
    indicated: list[ResourceRow]
    inferred: list[ResourceRow]


# ═══ 价格 ═══
class PricePoint(BaseModel):
    commodity: str       # "lithium_carbonate" | "copper" | "zinc" | "nickel"
    date: str            # "2026-06-28"
    price: float
    currency: str        # "USD" | "CNY"
    unit: str            # "USD/t" | "CNY/t"


# ═══ 日报 ═══
class DailyBrief(BaseModel):
    query: str
    generated_at: str
    news_summary: str
    resource_table: str   # Markdown table
    price_trend: str
    risk_alerts: str
    references: list[str]
    full_markdown: str
