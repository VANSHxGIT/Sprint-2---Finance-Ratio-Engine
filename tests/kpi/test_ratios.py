from src.Analytics.ratio import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    net_debt,
    asset_turnover,
)

print("ratios.py imported successfully")

print("NPM:", net_profit_margin(100, 500))
print("OPM:", operating_profit_margin(150, 500))
print("ROE:", return_on_equity(100, 200, 300))
print("ROCE:", return_on_capital_employed(150, 200, 300, 100))
print("ROA:", return_on_assets(100, 1000))
print("D/E:", debt_to_equity(100, 200, 300))
print("ICR:", interest_coverage_ratio(150, 20, 50))
print("Net Debt:", net_debt(500, 100))
print("Asset Turnover:", asset_turnover(1000, 500))