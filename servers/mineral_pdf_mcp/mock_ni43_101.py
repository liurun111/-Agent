"""mineral-pdf-mcp 内置 Mock NI 43-101 储量数据
基于真实报告的近似值：
  - Pilbara Minerals: Pilgangoora Project (2024 NI 43-101)
  - Newmont: Boddington Gold Mine
  - Barrick: Hemlo Gold Mine
"""
from datetime import date

REPORTS = {
    "pilgangoora": {
        "project": "Pilgangoora Lithium-Tantalum Project",
        "owner": "Pilbara Minerals Limited",
        "report_date": "2024-08-15",
        "pdf_url": "https://www.pilbaraminerals.com.au/ni43-101-pilgangoora-2024",
        "indicated": [
            {
                "category": "Indicated",
                "ore_tonnes_mt": 413.9,
                "grade": "1.15% Li2O",
                "metal_content": "4.76 Mt Li2O (11.8 Mt LCE)",
            },
        ],
        "inferred": [
            {
                "category": "Inferred",
                "ore_tonnes_mt": 95.1,
                "grade": "1.02% Li2O",
                "metal_content": "0.97 Mt Li2O (2.4 Mt LCE)",
            },
        ],
    },
    "boddington": {
        "project": "Boddington Gold-Copper Mine",
        "owner": "Newmont Corporation",
        "report_date": "2023-12-31",
        "pdf_url": "https://www.newmont.com/ni43-101-boddington-2023",
        "indicated": [
            {
                "category": "Indicated",
                "ore_tonnes_mt": 1007.0,
                "grade": "0.67 g/t Au, 0.11% Cu",
                "metal_content": "21.7 Moz Au, 1.11 Mt Cu",
            },
        ],
        "inferred": [
            {
                "category": "Inferred",
                "ore_tonnes_mt": 267.0,
                "grade": "0.52 g/t Au, 0.08% Cu",
                "metal_content": "4.5 Moz Au, 0.21 Mt Cu",
            },
        ],
    },
    "hemlo": {
        "project": "Hemlo Gold Mine",
        "owner": "Barrick Gold Corporation",
        "report_date": "2023-12-31",
        "pdf_url": "https://www.barrick.com/ni43-101-hemlo-2023",
        "indicated": [
            {
                "category": "Indicated",
                "ore_tonnes_mt": 102.3,
                "grade": "1.17 g/t Au",
                "metal_content": "3.85 Moz Au",
            },
        ],
        "inferred": [
            {
                "category": "Inferred",
                "ore_tonnes_mt": 25.7,
                "grade": "1.05 g/t Au",
                "metal_content": "0.87 Moz Au",
            },
        ],
    },
}


def resolve_report(pdf_url: str) -> dict | None:
    """URL → 报告数据；支持模糊匹配"""
    url_lower = pdf_url.lower()
    for key, report in REPORTS.items():
        if key in url_lower:
            return report
    # 中文/拼音匹配
    if "pilbara" in url_lower or "pilgangoora" in url_lower or "锂" in pdf_url:
        return REPORTS["pilgangoora"]
    if "boddington" in url_lower or "newmont" in url_lower or "金" in pdf_url:
        return REPORTS["boddington"]
    if "hemlo" in url_lower or "barrick" in url_lower:
        return REPORTS["hemlo"]
    return None
