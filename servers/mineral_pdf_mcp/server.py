"""mineral-pdf-mcp — NI 43-101 PDF 解析 MCP Server (FastMCP + SSE transport)
从 PDF 中提取 Indicated / Inferred Resources 表格数据。
"""
import sys, os, json, logging, re

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mineral-pdf-mcp")


def register_tools(mcp: FastMCP):
    from mock_ni43_101 import REPORTS, resolve_report as mock_resolve

    @mcp.tool()
    def extract_resources(pdf_url: str) -> str:
        """从 NI 43-101 矿权报告 PDF 提取 Indicated 和 Inferred Resources。
        支持本地 PDF 文件路径或 URL。
        返回: 项目名、矿石量(Mt)、品位(g/t 或 %)、金属量(oz 或 t)。

        Args:
            pdf_url: PDF 文件路径或 URL。传 "list" 列出内置报告。
        """
        if pdf_url.lower() == "list":
            available = [
                {"project": r["project"], "owner": r["owner"], "url": r["pdf_url"]}
                for r in REPORTS.values()
            ]
            return json.dumps(available, ensure_ascii=False, indent=2)

        # 1. 尝试真实 PDF 解析
        pdf_path = _resolve_path(pdf_url)
        if pdf_path and os.path.exists(pdf_path):
            logger.info(f"Parsing real PDF: {pdf_path}")
            result = _parse_ni43_101(pdf_path)
            if result and (result.get("indicated") or result.get("inferred")):
                logger.info(f"PDF parsed: {result['project']}")
                return json.dumps(result, ensure_ascii=False, indent=2)
            logger.warning(f"PDF parse returned empty, falling back to mock")

        # 2. Mock 兜底
        report = mock_resolve(pdf_url)
        if report:
            logger.info(f"Mock fallback: {report['project']}")
            return json.dumps({
                "project": report["project"],
                "owner": report["owner"],
                "report_date": report["report_date"],
                "pdf_url": report["pdf_url"],
                "indicated": report["indicated"],
                "inferred": report["inferred"],
                "_source": "mock (PDF not found or unparseable)",
            }, ensure_ascii=False, indent=2)

        known = ", ".join(REPORTS.keys())
        return json.dumps({
            "error": f"Report not found: '{pdf_url}'",
            "known_reports": known,
            "hint": "Pass 'list' for built-in reports, or provide a local PDF path.",
        }, ensure_ascii=False, indent=2)


def _resolve_path(url: str) -> str | None:
    """URL/路径 → 本地绝对路径"""
    p = url.strip().strip('"')
    if os.path.isabs(p) and os.path.exists(p):
        return p
    cwd_path = os.path.join(os.getcwd(), p)
    if os.path.exists(cwd_path):
        return cwd_path
    return None


def _parse_ni43_101(pdf_path: str) -> dict | None:
    """提取 NI 43-101 资源表格 — 先用 pypdf 提文本，pdfplumber 提表格（若有）"""
    full_text = ""
    tables = []

    # ── 方案1: pypdf 提取纯文本 ──
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"
        logger.info(f"pypdf extracted {len(full_text)} chars from {len(reader.pages)} pages")
    except Exception as e:
        logger.warning(f"pypdf failed: {e}")

    # ── 方案2: pdfplumber 提取表格（可选依赖） ──
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            if not full_text:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        full_text += t + "\n"
            for page in pdf.pages:
                for tbl in page.extract_tables():
                    if tbl:
                        tables.append(tbl)
        logger.info(f"pdfplumber found {len(tables)} tables")
    except ImportError:
        logger.info("pdfplumber not installed, using pypdf text only")
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}")

    if not full_text.strip():
        return None

    project = _extract_project(full_text)
    owner = _extract_owner(full_text)
    report_date = _extract_date(full_text)
    indicated, inferred = _extract_resources(full_text, tables)

    if indicated or inferred:
        source = "pypdf+pdfplumber" if tables else "pypdf (text parse)"
        return {
            "project": project or "Unknown",
            "owner": owner or "Unknown",
            "report_date": report_date or "Unknown",
            "pdf_url": pdf_path,
            "indicated": indicated,
            "inferred": inferred,
            "_source": source,
        }
    return None


def _extract_project(text: str) -> str | None:
    """从文本中提取项目名"""
    patterns = [
        r'(?:Project|Property|Mine|Deposit)\s*[:.]?\s*([A-Z][A-Za-z\s\-]+(?:Project|Mine|Deposit|Operation))',
        r'(?:NI\s*43\s*[-–]?\s*101)\s*(?:Technical\s*)?Report\s*:?\s*([A-Z][A-Za-z\s\-]+)',
        r'([A-Z][A-Za-z\s\-]+(?:Lithium|Gold|Copper|Zinc|Nickel)\s*(?:Project|Mine|Operation|Deposit))',
    ]
    for pat in patterns:
        m = re.search(pat, text[:3000])
        if m:
            return m.group(1).strip()
    # 第一行通常是标题
    first_line = text.strip().split("\n")[0]
    if len(first_line) > 5 and len(first_line) < 200:
        return first_line.strip()
    return None


def _extract_owner(text: str) -> str | None:
    """从文本中提取矿权人"""
    patterns = [
        r'(?:prepared\s*(?:by|for))\s*([A-Z][A-Za-z\s]+(?:Limited|Ltd|Corporation|Corp|Inc|Minerals|Resources|Gold|Mining))',
        r'(?:owner|operator)[:.]?\s*([A-Z][A-Za-z\s]+(?:Limited|Ltd|Corporation|Corp|Inc|Minerals|Resources))',
        r'([A-Z][A-Za-z\s]+(?:Minerals|Resources|Gold|Mining)\s*(?:Limited|Ltd|Corporation|Inc)?)',
    ]
    for pat in patterns:
        m = re.search(pat, text[:5000], re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _extract_date(text: str) -> str | None:
    """从文本中提取报告日期"""
    patterns = [
        r'(?:Effective\s*Date|Report\s*Date|As\s*of)[:.]?\s*(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(\d{4}[-/]\d{2}[-/]\d{2})',
    ]
    for pat in patterns:
        m = re.search(pat, text[:3000], re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _extract_resources(text: str, tables: list) -> tuple[list[dict], list[dict]]:
    """从文本和表格中提取 Indicated / Inferred 资源量"""
    indicated = []
    inferred = []

    # ── 方案A: 从 pdfplumber 表格解析 ──
    for table in tables:
        rows = _parse_resource_table(table)
        for row in rows:
            cat = row.get("category", "").lower()
            if "indicated" in cat and "measured" not in cat:
                indicated.append(row)
            elif "inferred" in cat:
                inferred.append(row)

    # ── 方案B: 从文本正则兜底 ──
    if not indicated and not inferred:
        indicated, inferred = _regex_parse(text)

    return indicated, inferred


def _parse_resource_table(table: list) -> list[dict]:
    """将 pdfplumber 表格行 → 结构化资源数据"""
    results = []
    if len(table) < 2:
        return results

    # 找表头行
    header_row = -1
    for i, row in enumerate(table):
        if row and any(
            h in str(c).lower() if c else False
            for h in ["category", "class", "tonnes", "grade", "indicated", "inferred", "矿石", "品位"]
        ):
            header_row = i
            break

    if header_row < 0:
        return results

    # 找列索引
    header = [str(c or "").lower().strip() for c in table[header_row]]
    col_map = _map_columns(header)

    for row in table[header_row + 1:]:
        if not row or all(c is None or str(c).strip() == "" for c in row):
            continue
        data = _parse_row(row, col_map)
        if data:
            results.append(data)

    return results


def _map_columns(header: list[str]) -> dict:
    """映射列名 → 索引"""
    m = {}
    for i, h in enumerate(header):
        h = h.lower().strip()
        if any(k in h for k in ["category", "classification", "class", "类别"]):
            m["category"] = i
        elif any(k in h for k in ["tonnes", "tonnage", "kt", "mt", "矿石量"]):
            m["tonnes"] = i
        elif any(k in h for k in ["grade", "品位"]):
            m["grade"] = i
        elif any(k in h for k in ["metal", "contained", "content", "金属量", "ounces", "oz", "li2o"]):
            m["metal"] = i
    return m


def _parse_row(row: list, col_map: dict) -> dict | None:
    """解析一行数据"""
    def _val(i):
        if i is None or i >= len(row):
            return ""
        v = row[i]
        return str(v).strip() if v else ""

    cat = _val(col_map.get("category"))
    if not cat:
        return None

    # 标准化类别名
    cat_lower = cat.lower()
    if "indicated" in cat_lower and "measured" not in cat_lower:
        category = "Indicated"
    elif "inferred" in cat_lower:
        category = "Inferred"
    elif "measured" in cat_lower:
        category = "Measured"
    else:
        category = cat

    # 矿石量
    tonnes_str = _val(col_map.get("tonnes"))
    ore_tonnes_mt = _parse_number(tonnes_str)

    grade = _val(col_map.get("grade"))
    metal = _val(col_map.get("metal"))

    if ore_tonnes_mt == 0 and not grade:
        return None

    return {
        "category": category,
        "ore_tonnes_mt": ore_tonnes_mt,
        "grade": grade or "—",
        "metal_content": metal or "—",
    }


def _parse_number(s: str) -> float:
    """'413.9' | '1,007 Mt' | '95.1 Mt' → float"""
    if not s:
        return 0.0
    s = re.sub(r'[,\s]', '', s)
    s = re.sub(r'(?i)(Mt|kt|t|tonnes|tons|oz|moz|koz).*$', '', s)
    try:
        return float(s)
    except ValueError:
        return 0.0


def _regex_parse(text: str) -> tuple[list[dict], list[dict]]:
    """正则兜底 — 从纯文本中匹配 NI 43-101 资源描述"""
    indicated = []
    inferred = []

    # NI 43-101 常见句式:
    # "Indicated Resources of X Mt grading Y% Li2O containing Z Mt Li2O"
    # "Indicated Mineral Resources: X Mt at Y g/t Au for Z Moz"
    patterns = [
        # 金矿: Indicated ... X Mt at Y g/t Au ... Z Moz
        (r'Indicated\s+(?:Mineral\s+)?Resources?\s*(?:of|:)?\s*([\d,.]+)\s*Mt\s*(?:at|@|grading)\s*([\d,.]+)\s*g/t\s*Au\s*(?:for|containing)?\s*([\d,.]+)\s*Moz', "Indicated"),
        # 锂矿: Indicated ... X Mt grading Y% Li2O ... Z Mt
        (r'Indicated\s+(?:Mineral\s+)?Resources?\s*(?:of|:)?\s*([\d,.]+)\s*Mt\s*(?:at|@|grading)\s*([\d,.]+)\s*%\s*Li\d*O\s*(?:for|containing)?\s*([\d,.]+)\s*Mt', "Indicated"),
        # Inferred 同上
        (r'Inferred\s+(?:Mineral\s+)?Resources?\s*(?:of|:)?\s*([\d,.]+)\s*Mt\s*(?:at|@|grading)\s*([\d,.]+)\s*g/t\s*Au\s*(?:for|containing)?\s*([\d,.]+)\s*Moz', "Inferred"),
        (r'Inferred\s+(?:Mineral\s+)?Resources?\s*(?:of|:)?\s*([\d,.]+)\s*Mt\s*(?:at|@|grading)\s*([\d,.]+)\s*%\s*Li\d*O\s*(?:for|containing)?\s*([\d,.]+)\s*Mt', "Inferred"),
    ]

    for pat, cat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            is_gold = "Moz" in pat
            entry = {
                "category": cat,
                "ore_tonnes_mt": _parse_number(m.group(1)),
                "grade": m.group(2).strip() + (" g/t Au" if is_gold else " % Li2O"),
            }
            entry["metal_content"] = f"{_parse_number(m.group(3)):.1f} Moz Au" if is_gold else f"{_parse_number(m.group(3)):.2f} Mt Li2O"
            if cat == "Indicated":
                indicated.append(entry)
            else:
                inferred.append(entry)

    return indicated, inferred


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "sse")
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8002"))

    mcp = FastMCP("mineral-pdf-mcp", host=host, port=port)
    register_tools(mcp)

    if transport == "sse":
        logger.info(f"Mineral PDF MCP Server -> SSE transport on {host}:{port}")
        mcp.run(transport="sse")
    else:
        logger.info("Mineral PDF MCP Server -> stdio transport")
        mcp.run(transport="stdio")
