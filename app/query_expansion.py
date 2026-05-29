import re

TERM_ALIASES = {
    "软件工程经济学": "software engineering economics SEE",
    "软件工程": "software engineering",
    "经济学": "economics",
    "软件成本": "software cost",
    "成本估算": "cost estimation software cost estimation",
    "规模估算": "size estimation software size measurement",
    "软件规模": "software size software size measurement",
    "功能点": "function point FP",
    "工作量估算": "effort estimation",
    "净现值": "net present value NPV",
    "期望净现值": "expected net present value ENPV",
    "内部收益率": "internal rate of return IRR",
    "投资回收期": "payback period",
    "盈亏平衡": "break-even analysis break-even point",
    "敏感性分析": "sensitivity analysis",
    "决策树": "decision tree",
    "风险": "risk",
    "不确定性": "uncertainty",
    "现金流": "cash flow",
    "现值": "present value PV",
    "终值": "future value FV",
    "折现": "discounting discount rate",
    "融资": "financing",
    "资金成本": "cost of capital",
    "折旧": "depreciation",
    "摊销": "amortization",
    "所得税": "income tax",
    "费用": "cost expense",
    "效益": "benefit",
    "供求": "supply demand",
    "定价": "pricing",
    "财务分析": "financial analysis",
    "现金流量表": "cash flow statement",
    "利润": "profit",
    "生命周期": "life cycle lifecycle",
    "软件质量": "software quality",
    "软件特性": "software characteristics",
    "经济主体": "economic agent stakeholder",
}


def expand_query(query: str) -> str:
    aliases = [alias for term, alias in TERM_ALIASES.items() if term in query]
    if not aliases:
        return query
    return query + "\n" + "\n".join(aliases)


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[一-鿿]", text))


def looks_english_document(kind: str, content: str, title: str) -> bool:
    if kind != "pdf_markdown":
        return False
    sample = (title + "\n" + content[:500]).strip()
    ascii_letters = len(re.findall(r"[A-Za-z]", sample))
    cjk = len(re.findall(r"[一-鿿]", sample))
    return ascii_letters > max(40, cjk * 2)
