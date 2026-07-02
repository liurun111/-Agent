"""lme-price-mcp 内置 Mock 价格数据 — 锂/铜/锌/镍 30天序列
基于真实价格区间模拟波动：
  - 碳酸锂 (CNY/t):       ~125,000 ± 8,000
  - 氢氧化锂 (CNY/t):      ~135,000 ± 10,000
  - 铜 LME (USD/t):        ~9,800 ± 300
  - 锌 LME (USD/t):        ~2,900 ± 120
  - 镍 LME (USD/t):        ~16,500 ± 800
  - 铁矿石 62% Fe (USD/t): ~115 ± 8
"""
import random
from datetime import date, timedelta

BASE_PRICES = {
    "lithium_carbonate":  {"price": 125_000, "currency": "CNY", "unit": "CNY/t"},
    "lithium_hydroxide":  {"price": 135_000, "currency": "CNY", "unit": "CNY/t"},
    "copper":             {"price":  9_800, "currency": "USD", "unit": "USD/t"},
    "zinc":               {"price":  2_900, "currency": "USD", "unit": "USD/t"},
    "nickel":             {"price": 16_500, "currency": "USD", "unit": "USD/t"},
    "iron_ore_62":        {"price":    115, "currency": "USD", "unit": "USD/dmt"},
}

# 日波动率 (standard deviation %)
DAILY_VOL = {
    "lithium_carbonate":  0.025,
    "lithium_hydroxide":  0.022,
    "copper":             0.012,
    "zinc":               0.014,
    "nickel":             0.018,
    "iron_ore_62":        0.015,
}

# 走势方向 (trend factor per day)
TREND = {
    "lithium_carbonate":  1.001,   # 温和上行
    "lithium_hydroxide":  1.0008,
    "copper":             0.9995,  # 微幅下行
    "zinc":               0.9998,
    "nickel":             1.002,   # 震荡上行
    "iron_ore_62":        0.9992,  # 小幅下行
}

random.seed(42)  # 可复现


def _generate_prices(commodity: str, days: int) -> list[dict]:
    """生成指定商品近 N 天价格序列"""
    base = BASE_PRICES.get(commodity)
    if base is None:
        return []
    vol = DAILY_VOL.get(commodity, 0.015)
    trend = TREND.get(commodity, 1.0)

    prices = []
    current = base["price"]
    for i in range(days, -1, -1):
        d = date.today() - timedelta(days=i)
        change = random.gauss(0, current * vol)
        current = current * trend + change
        current = max(current, base["price"] * 0.7)
        current = min(current, base["price"] * 1.3)
        prices.append({
            "commodity": commodity,
            "date": str(d),
            "price": round(current, 2),
            "currency": base["currency"],
            "unit": base["unit"],
        })
    return prices


# 预生成 30 天数据
PRICE_CACHE: dict[str, list[dict]] = {}
for c in BASE_PRICES:
    PRICE_CACHE[c] = _generate_prices(c, 30)
