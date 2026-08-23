"""
Financial Ratio Engine
----------------------
Sprint 2 - Epic 02

Contains profitability, leverage and efficiency ratio calculations.

All functions are designed to:
- handle zero/invalid denominators safely
- return None where the specification requires an undefined ratio
- avoid raising errors on missing financial data
- remain independently unit-testable
"""

from __future__ import annotations

from typing import Optional


def _safe_float(value) -> Optional[float]:
    """Convert a value to float, returning None for invalid/missing values."""
    if value is None:
        return None

    try:
        result = float(value)
    except (TypeError, ValueError):
        return None

    return result


# ============================================================
# PROFITABILITY RATIOS
# ============================================================

def net_profit_margin(
    net_profit,
    sales,
) -> Optional[float]:
    """
    Net Profit Margin (%).

    Formula:
        net_profit / sales * 100

    Returns None when sales is zero or unavailable.
    """
    net_profit = _safe_float(net_profit)
    sales = _safe_float(sales)

    if net_profit is None or sales in (None, 0):
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(
    operating_profit,
    sales,
) -> Optional[float]:
    """
    Operating Profit Margin (%).

    Formula:
        operating_profit / sales * 100

    Returns None when sales is zero or unavailable.
    """
    operating_profit = _safe_float(operating_profit)
    sales = _safe_float(sales)

    if operating_profit is None or sales in (None, 0):
        return None

    return (operating_profit / sales) * 100


def check_opm(
    computed_opm,
    source_opm,
    tolerance_pct: float = 1.0,
) -> bool:
    """
    Compare computed OPM with the source OPM.

    Returns True when the absolute difference is greater than
    the allowed tolerance.
    """
    computed_opm = _safe_float(computed_opm)
    source_opm = _safe_float(source_opm)

    if computed_opm is None or source_opm is None:
        return False

    return abs(computed_opm - source_opm) > tolerance_pct


def return_on_equity(
    net_profit,
    equity_capital,
    reserves,
) -> Optional[float]:
    """
    Return on Equity (ROE).

    Formula:
        net_profit / (equity_capital + reserves) * 100

    Returns None when total equity is zero or negative.
    """
    net_profit = _safe_float(net_profit)
    equity_capital = _safe_float(equity_capital)
    reserves = _safe_float(reserves)

    if None in (net_profit, equity_capital, reserves):
        return None

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
) -> Optional[float]:
    """
    Return on Capital Employed (ROCE).

    Formula:
        EBIT / (equity + reserves + borrowings) * 100

    Returns None when the capital employed denominator is zero.
    """
    ebit = _safe_float(ebit)
    equity_capital = _safe_float(equity_capital)
    reserves = _safe_float(reserves)
    borrowings = _safe_float(borrowings)

    if None in (ebit, equity_capital, reserves, borrowings):
        return None

    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed == 0:
        return None

    return (ebit / capital_employed) * 100


def return_on_assets(
    net_profit,
    total_assets,
) -> Optional[float]:
    """
    Return on Assets (ROA).

    Formula:
        net_profit / total_assets * 100

    Returns None when total assets are zero.
    """
    net_profit = _safe_float(net_profit)
    total_assets = _safe_float(total_assets)

    if net_profit is None or total_assets in (None, 0):
        return None

    return (net_profit / total_assets) * 100


# ============================================================
# LEVERAGE RATIOS
# ============================================================

def debt_to_equity(
    borrowings,
    equity_capital,
    reserves,
) -> Optional[float]:
    """
    Debt-to-Equity ratio.

    Formula:
        borrowings / (equity_capital + reserves)

    Special cases:
        - Debt-free company -> 0
        - Non-positive equity -> None
    """
    borrowings = _safe_float(borrowings)
    equity_capital = _safe_float(equity_capital)
    reserves = _safe_float(reserves)

    if None in (borrowings, equity_capital, reserves):
        return None

    if borrowings == 0:
        return 0.0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(
    de_ratio,
    broad_sector,
    threshold: float = 5.0,
) -> bool:
    """
    Flag companies with D/E > 5 outside the Financials sector.

    Financials are excluded because high leverage is structurally
    normal for banks, NBFCs and insurance companies.
    """
    de_ratio = _safe_float(de_ratio)

    if de_ratio is None:
        return False

    if str(broad_sector).strip().lower() == "financials":
        return False

    return de_ratio > threshold


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
) -> Optional[float]:
    """
    Interest Coverage Ratio (ICR).

    Formula:
        (operating_profit + other_income) / interest

    Returns None when interest is zero/unavailable.
    """
    operating_profit = _safe_float(operating_profit)
    other_income = _safe_float(other_income)
    interest = _safe_float(interest)

    if None in (operating_profit, other_income, interest):
        return None

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def interest_coverage_label(icr) -> str:
    """
    Display label for Interest Coverage Ratio.

    None indicates a debt-free / zero-interest company according
    to the Sprint 2 specification.
    """
    return "Debt Free" if icr is None else "Calculated"


def interest_coverage_warning(
    icr,
    threshold: float = 1.5,
) -> bool:
    """
    Flag companies whose ICR is below 1.5.
    """
    icr = _safe_float(icr)

    if icr is None:
        return False

    return icr < threshold


def net_debt(
    borrowings,
    investments,
) -> Optional[float]:
    """
    Net Debt.

    Formula:
        borrowings - investments

    Investments are treated as a liquid-asset proxy.
    """
    borrowings = _safe_float(borrowings)
    investments = _safe_float(investments)

    if None in (borrowings, investments):
        return None

    return borrowings - investments


# ============================================================
# EFFICIENCY
# ============================================================

def asset_turnover(
    sales,
    total_assets,
) -> Optional[float]:
    """
    Asset Turnover.

    Formula:
        sales / total_assets

    Returns None when total assets are zero.
    """
    sales = _safe_float(sales)
    total_assets = _safe_float(total_assets)

    if sales is None or total_assets in (None, 0):
        return None

    return sales / total_assets


# ============================================================
# BATCH CALCULATION
# ============================================================

def calculate_ratios(row) -> dict:
    """
    Calculate all Sprint 2 profitability, leverage and
    efficiency ratios for one company-year record.

    The function accepts either a pandas Series or a dictionary-like
    object containing the expected source columns.
    """

    get = row.get

    npm = net_profit_margin(
        get("net_profit"),
        get("sales"),
    )

    opm = operating_profit_margin(
        get("operating_profit"),
        get("sales"),
    )

    roe = return_on_equity(
        get("net_profit"),
        get("equity_capital"),
        get("reserves"),
    )

    roce = return_on_capital_employed(
        get("ebit", get("operating_profit")),
        get("equity_capital"),
        get("reserves"),
        get("borrowings"),
    )

    roa = return_on_assets(
        get("net_profit"),
        get("total_assets"),
    )

    de = debt_to_equity(
        get("borrowings"),
        get("equity_capital"),
        get("reserves"),
    )

    icr = interest_coverage_ratio(
        get("operating_profit"),
        get("other_income"),
        get("interest"),
    )

    nd = net_debt(
        get("borrowings"),
        get("investments"),
    )

    turnover = asset_turnover(
        get("sales"),
        get("total_assets"),
    )

    return {
        "net_profit_margin_pct": npm,
        "operating_profit_margin_pct": opm,
        "return_on_equity_pct": roe,
        "return_on_capital_employed_pct": roce,
        "return_on_assets_pct": roa,
        "debt_to_equity": de,
        "high_leverage_flag": high_leverage_flag(
            de,
            get("broad_sector"),
        ),
        "interest_coverage": icr,
        "icr_label": interest_coverage_label(icr),
        "icr_warning_flag": interest_coverage_warning(icr),
        "net_debt_cr": nd,
        "asset_turnover": turnover,
    }