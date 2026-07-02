"""mining-news-mcp 内置 Mock 新闻数据 — Pilbara 锂矿 + 锂电产业链，近30天"""
from datetime import date, timedelta

TODAY = str(date.today())
_day = lambda d: str(date.today() - timedelta(days=d))

NEWS = [
    {
        "title": "Pilbara Minerals ramps up Pilgangoora expansion to 1Mtpa",
        "summary": "Pilbara Minerals announced the P2000 expansion project reached 85% completion, targeting 1Mtpa spodumene concentrate capacity by Q4 2026.",
        "source": "mining.com",
        "date": _day(2),
        "url": "https://www.mining.com/pilbara-minerals-ramps-pilgangoora-expansion"
    },
    {
        "title": "Lithium carbonate prices rebound 8% on Chinese spot market",
        "summary": "Battery-grade lithium carbonate in China rose to 125,000 CNY/t, up 8% week-on-week, driven by cathode restocking ahead of Q3 EV production push.",
        "source": "Shanghai Metals Market",
        "date": _day(1),
        "url": "https://www.metal.com/lithium-carbonate-price-rebound"
    },
    {
        "title": "Australia designates lithium as critical mineral under new strategy",
        "summary": "The Australian government released its 2026 Critical Minerals Strategy update, adding lithium processing to the priority list with A$2bn in loan guarantees.",
        "source": "DISR Australia",
        "date": _day(5),
        "url": "https://www.industry.gov.au/critical-minerals-strategy-2026"
    },
    {
        "title": "Pilbara Minerals signs offtake deal with Chinese cathode maker",
        "summary": "A new 5-year offtake agreement was signed between Pilbara Minerals and a top-5 Chinese cathode producer for 150ktpa spodumene concentrate.",
        "source": "Reuters",
        "date": _day(4),
        "url": "https://www.reuters.com/pilbara-minerals-offtake-china"
    },
    {
        "title": "WA government fast-tracks Pilbara lithium infrastructure",
        "summary": "The Western Australian government committed A$500m to upgrade port and road infrastructure in Port Hedland to support lithium export growth.",
        "source": "ABC News",
        "date": _day(7),
        "url": "https://www.abc.net.au/wa-pilbara-lithium-infrastructure"
    },
    {
        "title": "S&P Global raises lithium price forecast for H2 2026",
        "summary": "S&P Global Commodity Insights revised its H2 2026 lithium price forecast upward by 12%, citing stronger-than-expected EV sales in China and Europe.",
        "source": "S&P Global",
        "date": _day(3),
        "url": "https://www.spglobal.com/lithium-forecast-h2-2026"
    },
    {
        "title": "赣锋锂业与Pilbara Minerals探讨下游合资",
        "summary": "赣锋锂业透露正与Pilbara Minerals就西澳锂盐加工合资进行尽职调查，拟投资5亿美元建设氢氧化锂工厂。",
        "source": "中国稀土集团官网",
        "date": _day(6),
        "url": "https://www.gfli.com/pilbara-jv-talks"
    },
    {
        "title": "LME launches lithium carbonate futures contract",
        "summary": "The London Metal Exchange launched a new lithium carbonate futures contract, with first-day trading volume exceeding 2,000 lots.",
        "source": "LME",
        "date": _day(9),
        "url": "https://www.lme.com/lithium-carbonate-futures-launch"
    },
    {
        "title": "Pilbara Minerals Q2 production beats guidance by 8%",
        "summary": "Pilbara Minerals reported Q2 2026 spodumene production of 178kt, beating guidance of 165kt, with an average realised price of US$1,850/t SC6.",
        "source": "Pilbara Minerals ASX",
        "date": _day(8),
        "url": "https://www.pilbaraminerals.com.au/quarterly-report-q2-2026"
    },
    {
        "title": "Chile lithium nationalisation debate spooks investors",
        "summary": "Chile's Congress resumed debate on lithium nationalisation, causing Albemarle and SQM shares to drop 6%, potentially benefiting Australian producers like Pilbara Minerals.",
        "source": "Financial Times",
        "date": _day(10),
        "url": "https://www.ft.com/chile-lithium-nationalisation"
    },
    {
        "title": "CATL sodium-ion battery milestone raises lithium demand questions",
        "summary": "CATL announced mass production of second-gen sodium-ion batteries at 160Wh/kg, but analysts say lithium remains irreplaceable for high-nickel EV applications.",
        "source": "Bloomberg",
        "date": _day(12),
        "url": "https://www.bloomberg.com/catl-sodium-ion-2026"
    },
    {
        "title": "Pilgangoora resource update adds 15% to Measured category",
        "summary": "An updated NI 43-101 technical report upgraded 50Mt from Indicated to Measured Resources at Pilgangoora, extending mine life to 36 years.",
        "source": "mining.com",
        "date": _day(14),
        "url": "https://www.mining.com/pilgangoora-resource-update"
    },
    {
        "title": "European lithium refinery startup secures €300m funding",
        "summary": "A new lithium refinery in Germany secured €300m in Series C funding to process Australian spodumene into battery-grade hydroxide for European EV makers.",
        "source": "Reuters",
        "date": _day(15),
        "url": "https://www.reuters.com/europe-lithium-refinery-funding"
    },
    {
        "title": "中国锂盐库存降至三个月新低",
        "summary": "SMM数据显示，中国碳酸锂社会库存降至约4.2万吨，为三个月新低，下游正极材料厂采购积极。",
        "source": "上海有色网",
        "date": _day(11),
        "url": "https://www.smm.cn/lithium-inventory-low"
    },
    {
        "title": "Pilbara Minerals to trial direct lithium extraction technology",
        "summary": "Pilbara Minerals partnered with EnergySource Minerals to trial DLE technology at Pilgangoora, aiming to reduce processing time from 18 months to 30 days.",
        "source": "mining.com",
        "date": _day(16),
        "url": "https://www.mining.com/pilbara-dle-trial"
    },
    {
        "title": "Australia lithium export revenue forecast to hit A$20bn in FY2027",
        "summary": "The Australian Department of Industry forecast lithium export earnings to reach A$20bn in FY2027, up from A$16bn in FY2026, driven by volume growth.",
        "source": "DISR Australia",
        "date": _day(18),
        "url": "https://www.industry.gov.au/lithium-export-forecast"
    },
    {
        "title": "低压锂电储能系统需求激增，Pilbara锂精矿受益",
        "summary": "中国储能市场H1 2026装机量同比增长45%，拉动锂电需求，Pilbara锂精矿现货溢价扩大。",
        "source": "高工锂电",
        "date": _day(13),
        "url": "https://www.gg-lb.com/energy-storage-demand-lithium"
    },
    {
        "title": "Rio Tinto eyes lithium acquisition in Pilbara region",
        "summary": "Rio Tinto is reportedly evaluating lithium tenement acquisitions near Pilgangoora, signalling major miner interest in the Pilbara lithium belt.",
        "source": "Australian Financial Review",
        "date": _day(20),
        "url": "https://www.afr.com/rio-tinto-pilbara-lithium"
    },
    {
        "title": "Tesla Megafactory Shanghai to double lithium demand from China",
        "summary": "Tesla's Shanghai Megafactory expansion will require an additional 25kt of lithium carbonate equivalent per year, tightening the Asia-Pacific supply balance.",
        "source": "Bloomberg",
        "date": _day(21),
        "url": "https://www.bloomberg.com/tesla-shanghai-lithium-demand"
    },
    {
        "title": "Pilbara Minerals completes A$300m placement for expansion",
        "summary": "Pilbara Minerals successfully completed a A$300m institutional placement at A$4.20/share to fund the next phase of Pilgangoora expansion.",
        "source": "Pilbara Minerals ASX",
        "date": _day(22),
        "url": "https://www.pilbaraminerals.com.au/placement-completed"
    },
    {
        "title": "Japan establishes lithium stockpile program",
        "summary": "Japan's METI announced a national lithium stockpile program targeting 30 days of import cover, joining South Korea and the EU in securing battery metal supply.",
        "source": "Nikkei Asia",
        "date": _day(25),
        "url": "https://asia.nikkei.com/japan-lithium-stockpile"
    },
    {
        "title": "Lithium hydroxide premium over carbonate widens",
        "summary": "The hydroxide-to-carbonate premium widened to US$3,800/t in June, reflecting strong demand for high-nickel cathode chemistries and tight hydroxide supply.",
        "source": "Benchmark Mineral Intelligence",
        "date": _day(17),
        "url": "https://www.benchmarkminerals.com/hydroxide-premium"
    },
    {
        "title": "印尼镍矿政策转向或影响三元电池供应链",
        "summary": "印尼政府拟对镍矿出口加征10%附加税，推高NCM三元成本，间接增强LFP及Pilbara锂精矿的竞争力。",
        "source": "中国有色金属报",
        "date": _day(19),
        "url": "https://www.cnnm.com.cn/indonesia-nickel-policy"
    },
    {
        "title": "Pilbara Minerals ESG rating upgraded by MSCI",
        "summary": "MSCI upgraded Pilbara Minerals' ESG rating from BBB to A, citing improved water management and community engagement at Pilgangoora operations.",
        "source": "MSCI",
        "date": _day(24),
        "url": "https://www.msci.com/pilbara-minerals-esg-upgrade"
    },
    {
        "title": "中国工信部发布锂电行业规范条件修订版",
        "summary": "工信部修订锂离子电池行业规范条件，提高锂回收率要求至95%以上，利好具备回收技术的锂盐企业。",
        "source": "工信部",
        "date": _day(27),
        "url": "https://www.miit.gov.cn/lithium-battery-regulation"
    },
    {
        "title": "Korean battery makers lock in long-term lithium supply",
        "summary": "LG Energy Solution and SK On each signed 7-year lithium supply agreements with Australian producers, totalling 300kt of spodumene annually.",
        "source": "Reuters",
        "date": _day(23),
        "url": "https://www.reuters.com/korea-battery-lithium-supply"
    },
    {
        "title": "Pilbara lithium train derailment causes minor supply disruption",
        "summary": "A minor train derailment near Port Hedland delayed lithium concentrate shipments by 48 hours; Pilbara Minerals says no impact on quarterly guidance.",
        "source": "ABC News",
        "date": _day(26),
        "url": "https://www.abc.net.au/pilbara-train-derailment"
    },
    {
        "title": "Global lithium-ion battery recycling capacity to triple by 2028",
        "summary": "A Benchmark report projects global Li-ion battery recycling capacity will triple by 2028, potentially supplying 15% of lithium demand from secondary sources.",
        "source": "Benchmark Mineral Intelligence",
        "date": _day(28),
        "url": "https://www.benchmarkminerals.com/recycling-capacity-2028"
    },
]

FULL_TEXT = {
    "https://www.mining.com/pilbara-minerals-ramps-pilgangoora-expansion": (
        "Pilbara Minerals Ltd (ASX: PLS) announced today that its P2000 expansion project at the "
        "Pilgangoora lithium-tantalum operation in Western Australia has reached 85% completion. "
        "The expansion targets 1 million tonnes per annum (Mtpa) of spodumene concentrate production "
        "capacity by Q4 2026, up from the current 680ktpa. CEO Dale Henderson stated: 'The P2000 "
        "expansion is tracking on schedule and under budget. When complete, Pilgangoora will be the "
        "largest independent hard-rock lithium mine in the world.' The company also reported that "
        "commissioning of the new flotation circuit will begin in September 2026. Capital expenditure "
        "for the expansion is estimated at A$560m, with A$420m already committed."
    ),
    "https://www.reuters.com/pilbara-minerals-offtake-china": (
        "Pilbara Minerals has signed a binding 5-year offtake agreement with a top-5 Chinese cathode "
        "material producer for the supply of 150,000 tonnes per annum of spodumene concentrate (SC6). "
        "The pricing mechanism is linked to the average of Fastmarkets and SMM lithium carbonate indices, "
        "with a floor price of US$1,200/t and ceiling of US$2,500/t SC6. The contract includes a "
        "prepayment facility of US$50m to support Pilbara Minerals' working capital during the P2000 "
        "expansion. Deliveries will commence from January 2027."
    ),
    "https://www.pilbaraminerals.com.au/quarterly-report-q2-2026": (
        "Pilbara Minerals Q2 FY2026 (October-December 2025) Quarterly Report highlights: Spodumene "
        "concentrate production of 178,000 dry metric tonnes (dmt), exceeding guidance of 165,000 dmt. "
        "Average realised price of US$1,850/dmt SC6 (CIF China). Unit operating cost of A$525/dmt, "
        "down 12% quarter-on-quarter. Shipping volume of 195,000 dmt. Cash balance of A$1.2bn at "
        "quarter end. FY2026 production guidance maintained at 680,000-720,000 dmt."
    ),
    "https://www.mining.com/pilgangoora-resource-update": (
        "An updated NI 43-101 compliant Mineral Resource estimate for the Pilgangoora Project was "
        "released today. Total Measured and Indicated Resources now stand at 414Mt grading 1.15% Li2O, "
        "containing 4.76Mt of Li2O. Inferred Resources total 95Mt grading 1.02% Li2O, containing "
        "0.97Mt of Li2O. The update converted 50Mt from the Indicated to Measured category following "
        "infill drilling. Mine life has been extended to 36 years based on the updated resource model."
    ),
}
