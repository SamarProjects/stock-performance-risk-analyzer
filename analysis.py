import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# =========================
# 1. PROJECT SETTINGS
# =========================

stock_ticker = "AAPL"
benchmark_ticker = "^GSPC"

start_date = "2021-01-01"
end_date = "2026-01-01"

years = 5


# =========================
# 2. DOWNLOAD MARKET DATA
# =========================

apple_data = yf.download(
    stock_ticker,
    start=start_date,
    end=end_date,
    progress=False
)

sp500_data = yf.download(
    benchmark_ticker,
    start=start_date,
    end=end_date,
    progress=False
)


# =========================
# 3. PREPARE PRICE DATA
# =========================

apple_close = apple_data["Close"][stock_ticker]
sp500_close = sp500_data["Close"][benchmark_ticker]

prices = pd.DataFrame({
    "Apple": apple_close,
    "S&P 500": sp500_close
})

prices.to_csv("data/market_prices.csv")

missing_values = prices.isnull().sum()

prices = prices.dropna()


# =========================
# 4. DAILY RETURNS
# =========================

daily_returns = prices.pct_change().dropna()


# =========================
# 5. CUMULATIVE RETURNS
# =========================

cumulative_returns = (1 + daily_returns).cumprod() - 1

final_cumulative_return = cumulative_returns.iloc[-1]


# =========================
# 6. ANNUALIZED RETURN
# =========================

annualized_return = (
    (1 + final_cumulative_return) ** (1 / years)
) - 1


# =========================
# 7. VOLATILITY
# =========================

daily_volatility = daily_returns.std()

annualized_volatility = (
    daily_volatility * (252 ** 0.5)
)


# =========================
# 8. DRAWDOWN
# =========================

running_max = prices.cummax()

drawdown = prices / running_max - 1

max_drawdown = drawdown.min()


# =========================
# 9. RETURN-TO-VOLATILITY
# =========================

return_to_volatility = (
    annualized_return / annualized_volatility
)


# =========================
# 10. ANNUAL RETURNS
# =========================

annual_returns = (
    (1 + daily_returns)
    .groupby(daily_returns.index.year)
    .prod()
    - 1
)

best_year = annual_returns.idxmax()
worst_year = annual_returns.idxmin()

best_year_return = annual_returns.max()
worst_year_return = annual_returns.min()


# =========================
# 11. BENCHMARK COMPARISON
# =========================

excess_annualized_return = (
    annualized_return["Apple"]
    - annualized_return["S&P 500"]
)

correlation = daily_returns["Apple"].corr(
    daily_returns["S&P 500"]
)

beta = (
    daily_returns["Apple"].cov(
        daily_returns["S&P 500"]
    )
    / daily_returns["S&P 500"].var()
)


# =========================
# 12. DISPLAY RESULTS
# =========================

print("\n--- PERFORMANCE ---")

print(
    f"Apple Cumulative Return: "
    f"{final_cumulative_return['Apple']:.2%}"
)

print(
    f"S&P 500 Cumulative Return: "
    f"{final_cumulative_return['S&P 500']:.2%}"
)

print(
    f"Apple Annualized Return: "
    f"{annualized_return['Apple']:.2%}"
)

print(
    f"S&P 500 Annualized Return: "
    f"{annualized_return['S&P 500']:.2%}"
)


print("\n--- RISK ---")

print(
    f"Apple Annualized Volatility: "
    f"{annualized_volatility['Apple']:.2%}"
)

print(
    f"S&P 500 Annualized Volatility: "
    f"{annualized_volatility['S&P 500']:.2%}"
)

print(
    f"Apple Maximum Drawdown: "
    f"{max_drawdown['Apple']:.2%}"
)

print(
    f"S&P 500 Maximum Drawdown: "
    f"{max_drawdown['S&P 500']:.2%}"
)


print("\n--- RISK-ADJUSTED PERFORMANCE ---")

print(
    f"Apple Return-to-Volatility Ratio: "
    f"{return_to_volatility['Apple']:.2f}"
)

print(
    f"S&P 500 Return-to-Volatility Ratio: "
    f"{return_to_volatility['S&P 500']:.2f}"
)


print("\n--- ANNUAL PERFORMANCE ---")

print(
    f"Apple Best Year: {best_year['Apple']} "
    f"({best_year_return['Apple']:.2%})"
)

print(
    f"Apple Worst Year: {worst_year['Apple']} "
    f"({worst_year_return['Apple']:.2%})"
)

print(
    f"S&P 500 Best Year: {best_year['S&P 500']} "
    f"({best_year_return['S&P 500']:.2%})"
)

print(
    f"S&P 500 Worst Year: {worst_year['S&P 500']} "
    f"({worst_year_return['S&P 500']:.2%})"
)


print("\n--- BENCHMARK COMPARISON ---")

print(
    f"Apple Excess Annualized Return: "
    f"{excess_annualized_return:.2%}"
)

print(
    f"Apple / S&P 500 Correlation: "
    f"{correlation:.2f}"
)

print(
    f"Apple Beta: "
    f"{beta:.2f}"
)


print("\n--- DATA QUALITY ---")

print("Missing Values Before Cleaning:")
print(missing_values)


# =========================
# 13. VISUALIZATIONS
# =========================


# -------------------------
# Chart 1: Cumulative Returns
# -------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    cumulative_returns.index,
    cumulative_returns["Apple"],
    label="Apple"
)

plt.plot(
    cumulative_returns.index,
    cumulative_returns["S&P 500"],
    label="S&P 500"
)

plt.title("Cumulative Return: Apple vs S&P 500")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.tight_layout()

plt.savefig("charts/cumulative_returns.png")
plt.close()


# -------------------------
# Chart 2: Drawdown
# -------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    drawdown.index,
    drawdown["Apple"],
    label="Apple"
)

plt.plot(
    drawdown.index,
    drawdown["S&P 500"],
    label="S&P 500"
)

plt.title("Drawdown: Apple vs S&P 500")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.legend()
plt.tight_layout()

plt.savefig("charts/drawdown.png")
plt.close()


# -------------------------
# Chart 3: Annual Returns
# -------------------------

annual_returns_percent = annual_returns * 100

x = range(len(annual_returns_percent.index))

plt.figure(figsize=(10, 6))

plt.bar(
    [i - 0.2 for i in x],
    annual_returns_percent["Apple"],
    width=0.4,
    label="Apple"
)

plt.bar(
    [i + 0.2 for i in x],
    annual_returns_percent["S&P 500"],
    width=0.4,
    label="S&P 500"
)

plt.title("Annual Returns: Apple vs S&P 500")
plt.xlabel("Year")
plt.ylabel("Return (%)")
plt.xticks(
    x,
    annual_returns_percent.index
)
plt.legend()
plt.tight_layout()

plt.savefig("charts/annual_returns.png")
plt.close()


# -------------------------
# Chart 4: Risk vs Return
# -------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    annualized_volatility["Apple"] * 100,
    annualized_return["Apple"] * 100,
    s=100
)

plt.scatter(
    annualized_volatility["S&P 500"] * 100,
    annualized_return["S&P 500"] * 100,
    s=100
)

plt.text(
    annualized_volatility["Apple"] * 100,
    annualized_return["Apple"] * 100,
    " Apple"
)

plt.text(
    annualized_volatility["S&P 500"] * 100,
    annualized_return["S&P 500"] * 100,
    " S&P 500"
)

plt.title("Risk vs Return: Apple vs S&P 500")
plt.xlabel("Annualized Volatility (%)")
plt.ylabel("Annualized Return (%)")
plt.tight_layout()

plt.savefig("charts/risk_vs_return.png")
plt.close()


# -------------------------
# Chart 5: Daily Return Relationship
# -------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    daily_returns["S&P 500"] * 100,
    daily_returns["Apple"] * 100,
    alpha=0.4
)

plt.title("Daily Returns: Apple vs S&P 500")
plt.xlabel("S&P 500 Daily Return (%)")
plt.ylabel("Apple Daily Return (%)")
plt.tight_layout()

plt.savefig(
    "charts/daily_returns_scatter.png"
)

plt.close()


print(
    "\nCharts successfully created "
    "in the charts folder."
)