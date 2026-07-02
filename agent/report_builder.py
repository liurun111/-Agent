"""简报模板 — 从工具返回数据渲染 Markdown"""
import json
from datetime import date


def build_report(query: str, news_data: list[dict], resource_data: dict | None,
                 trend_data: dict | None) -> str:
    """拼接 Markdown 简报"""

    today = str(date.today())
    lines = [
        f"# 矿权日报",
        f"**日期**: {today}  |  **查询**: {query}",
        "",
        "---",
        "",
    ]

    # ── 一、新闻摘要 ──
    lines.append("## 一、近期新闻摘要")
    lines.append("")
    if news_data:
        for i, item in enumerate(news_data[:8], 1):
            lines.append(f"{i}. **{item['title']}** — {item['summary'][:120]}（[{item['source']}]({item['url']})）")
            lines.append("")
    else:
        lines.append("*无相关新闻数据*")
        lines.append("")

    # ── 二、NI 43-101 储量 ──
    lines.append("---")
    lines.append("")
    lines.append("## 二、NI 43-101 资源储量")
    lines.append("")
    if resource_data and "error" not in resource_data:
        project = resource_data.get("project", "Unknown")
        lines.append(f"**项目**: {project}  |  **矿权人**: {resource_data.get('owner', 'N/A')}  |  **报告日期**: {resource_data.get('report_date', 'N/A')}")
        lines.append("")
        lines.append("| 项目 | 类别 | 矿石量 (Mt) | 品位 | 金属量 |")
        lines.append("|------|------|-------------|------|--------|")
        for row in resource_data.get("indicated", []):
            lines.append(f"| {project} | {row['category']} | {row['ore_tonnes_mt']:.1f} | {row['grade']} | {row['metal_content']} |")
        for row in resource_data.get("inferred", []):
            lines.append(f"| {project} | {row['category']} | {row['ore_tonnes_mt']:.1f} | {row['grade']} | {row['metal_content']} |")
        lines.append("")
    else:
        lines.append("*储量数据不可用*")
        lines.append("")

    # ── 三、价格走势 ──
    lines.append("---")
    lines.append("")
    lines.append("## 三、价格走势（近30日）")
    lines.append("")
    if trend_data and "error" not in trend_data:
        lines.append("| 商品 | 起始价 | 当前价 | 涨跌幅 | 30日最高 | 30日最低 |")
        lines.append("|------|--------|--------|--------|----------|----------|")
        currency = trend_data.get("currency", "USD")
        unit = trend_data.get("unit", "")
        lines.append(
            f"| {trend_data.get('commodity', 'N/A')} "
            f"| {trend_data.get('start_price', 0):,.0f} "
            f"| {trend_data.get('end_price', 0):,.0f} "
            f"| {trend_data.get('change_pct', 0):+.1f}% "
            f"| {trend_data.get('high', 0):,.0f} "
            f"| {trend_data.get('low', 0):,.0f} |"
        )
        lines.append("")
        lines.append(f"*单位: {currency} {unit}*")
        lines.append("")
    else:
        lines.append("*价格数据不可用*")
        lines.append("")

    # ── 四、风险提示 ──
    lines.append("---")
    lines.append("")
    lines.append("## 四、风险提示")
    lines.append("")
    risks = _infer_risks(news_data, trend_data)
    for risk in risks:
        lines.append(f"- **{risk['title']}**: {risk['detail']}")
    lines.append("")

    # ── 五、数据来源 ──
    lines.append("---")
    lines.append("")
    lines.append("## 五、数据来源")
    lines.append("")
    seen = set()
    idx = 1
    for item in (news_data or [])[:8]:
        if item["url"] not in seen:
            seen.add(item["url"])
            lines.append(f"{idx}. [{item['source']}]({item['url']}) — {item['title']}")
            idx += 1
    if resource_data and "error" not in resource_data:
        pdf_url = resource_data.get("pdf_url", "")
        if pdf_url and pdf_url not in seen:
            lines.append(f"{idx}. [NI 43-101 Technical Report]({pdf_url})")
            idx += 1
    lines.append("")

    return "\n".join(lines)


def _infer_risks(news_data: list[dict], trend_data: dict | None) -> list[dict]:
    """基于新闻和价格数据推理风险"""
    risks = []
    all_text = " ".join([item.get("title", "") + " " + item.get("summary", "") for item in (news_data or [])]).lower()

    if "nationalisation" in all_text or "nationalization" in all_text or "国有化" in all_text:
        risks.append({"title": "资源民族主义风险", "detail": "产锂国政策变动可能导致供应中断或成本上升（参考智利锂矿国有化讨论）。"})

    if trend_data and "error" not in trend_data:
        c = trend_data.get("change_pct", 0)
        if c < -5:
            risks.append({"title": "价格下行风险", "detail": f"近30日价格跌幅达{abs(c):.1f}%，需关注库存积压和下游需求变化。"})
        elif c > 10:
            risks.append({"title": "价格过热风险", "detail": f"近30日价格涨幅达{c:.1f}%，警惕投机性囤货和回调风险。"})

    if "derailment" in all_text or "disruption" in all_text or "中断" in all_text:
        risks.append({"title": "物流中断风险", "detail": "运输中断事件（如Pilbara铁路事故）可能导致短期供应波动。"})

    if "policy" in all_text or "regulation" in all_text or "政策" in all_text or "规范" in all_text:
        risks.append({"title": "政策变动风险", "detail": "关键矿产政策调整可能影响矿山审批、出口配额或加工补贴。"})

    if len(risks) < 2:
        risks.append({"title": "地缘政治风险", "detail": "全球贸易摩擦和供应链重组可能影响锂精矿进出口和定价机制。"})

    return risks[:4]
