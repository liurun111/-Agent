"""lme-price-mcp — 金属价格查询 MCP Server (FastMCP + SSE transport)"""
import sys, os, json, logging

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lme-price-mcp")

SUPPORTED = ["lithium_carbonate", "lithium_hydroxide", "copper", "zinc", "nickel", "iron_ore_62"]


def register_tools(mcp: FastMCP):
    from mock_prices import BASE_PRICES, PRICE_CACHE

    @mcp.tool()
    def get_price(commodity: str, date: str) -> str:
        """查询指定商品在指定日期的收盘价。

        Args:
            commodity: 商品名称，支持: lithium_carbonate, lithium_hydroxide, copper, zinc, nickel, iron_ore_62
            date: 日期，格式YYYY-MM-DD，例如 "2026-06-28"
        """
        commodity = commodity.lower().strip()
        if commodity not in PRICE_CACHE:
            return json.dumps(
                {"error": f"Unknown commodity '{commodity}'.", "supported": SUPPORTED},
                ensure_ascii=False,
            )

        prices = PRICE_CACHE[commodity]
        for p in prices:
            if p["date"] == date:
                logger.info(f"get_price({commodity}, {date}) -> {p['price']} {p['unit']}")
                return json.dumps(p, ensure_ascii=False, indent=2)

        return json.dumps(
            {"error": f"No data for {commodity} on {date}.", "available_range": f"{prices[0]['date']} to {prices[-1]['date']}"},
            ensure_ascii=False,
        )

    @mcp.tool()
    def get_trend(commodity: str, days: int = 30) -> str:
        """查询指定商品近N天的价格走势，返回完整序列及涨跌统计。

        Args:
            commodity: 商品名称，支持: lithium_carbonate, lithium_hydroxide, copper, zinc, nickel, iron_ore_62
            days: 查询天数，默认30天
        """
        commodity = commodity.lower().strip()
        if commodity not in PRICE_CACHE:
            return json.dumps(
                {"error": f"Unknown commodity '{commodity}'.", "supported": SUPPORTED},
                ensure_ascii=False,
            )

        all_prices = PRICE_CACHE[commodity]
        prices = all_prices[-days:] if days < len(all_prices) else all_prices

        first = prices[0]["price"]
        last = prices[-1]["price"]
        change = last - first
        change_pct = (change / first) * 100

        high = max(p["price"] for p in prices)
        low = min(p["price"] for p in prices)

        stats = {
            "commodity": commodity,
            "period_days": len(prices),
            "start_date": prices[0]["date"],
            "end_date": prices[-1]["date"],
            "start_price": first,
            "end_price": last,
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "currency": prices[0]["currency"],
            "unit": prices[0]["unit"],
            "prices": prices,
        }

        logger.info(f"get_trend({commodity}, {days}) -> {change_pct:+.2f}%")
        return json.dumps(stats, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "sse")
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8003"))

    mcp = FastMCP("lme-price-mcp", host=host, port=port)
    register_tools(mcp)

    if transport == "sse":
        logger.info(f"LME Price MCP Server -> SSE transport on {host}:{port}")
        mcp.run(transport="sse")
    else:
        logger.info("LME Price MCP Server -> stdio transport")
        mcp.run(transport="stdio")
