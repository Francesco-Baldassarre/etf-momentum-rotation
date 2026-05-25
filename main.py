import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set up
tickers = ["SPY", "QQQ", "EFA", "EEM", "TLT", "GLD"]

LOOKBACK_MOMENTUM = 60
LOOKBACK_VOL = 20
REBALANCE_FREQ = "ME"
TCOST = 0.001
INITIAL_CAPITAL = 100

# data 
data = yf.download(tickers, period="20y", auto_adjust=True, progress=False)["Close"]
data = data.ffill().dropna()
returns = data.pct_change().dropna()

# momentum signal
momentum = data / data.shift(LOOKBACK_MOMENTUM) - 1
vol = returns.rolling(LOOKBACK_VOL).std() * np.sqrt(252)

signal = momentum / (vol + 1e-8)
signal = signal.replace([np.inf, -np.inf], np.nan).clip(lower=0)

# weights
weights_daily = signal.div(signal.sum(axis=1), axis=0)
weights = (weights_daily.resample(REBALANCE_FREQ).last().reindex(returns.index).ffill())
weights = weights.shift(1).fillna(0)

# returns & costs
turnover = weights.diff().abs().sum(axis=1)
costs = turnover * TCOST

strategy_returns = (weights * returns).sum(axis=1) - costs
spy_returns = returns["SPY"]

# exclude initial estimation period (momentum lookback)
start_date = strategy_returns.index[LOOKBACK_MOMENTUM]
strategy_returns = strategy_returns.loc[start_date:]
spy_returns = spy_returns.loc[start_date:]
weights = weights.loc[start_date:]

spy_returns = spy_returns.loc[strategy_returns.index]

# equity curves
strategy_curve = INITIAL_CAPITAL * (1 + strategy_returns).cumprod()
spy_curve = INITIAL_CAPITAL * (1 + spy_returns).cumprod()


# DD
strategy_dd = strategy_curve / strategy_curve.cummax() - 1
spy_dd = spy_curve / spy_curve.cummax() - 1

# performances 
def CAGR(curve):
    years = len(curve) / 252
    return (curve.iloc[-1] / curve.iloc[0]) ** (1 / years) - 1

def sharpe(ret):
    return np.sqrt(252) * ret.mean() / ret.std()

def max_dd(dd):
    return dd.min()

print("PERFORMANCE METRICS")
print("********************")

print("ETF Rotation Strategy")
print(f"CAGR: {CAGR(strategy_curve):.2%}")
print(f"Sharpe: {sharpe(strategy_returns):.2f}")
print(f"Max Drawdown: {max_dd(strategy_dd):.2%}")

print("SPY")
print(f"CAGR: {CAGR(spy_curve):.2%}")
print(f"Sharpe: {sharpe(spy_returns):.2f}")
print(f"Max Drawdown: {max_dd(spy_dd):.2%}")

# Equity curves plot
plt.figure(figsize=(12,6))
strategy_curve.plot(label="ETF Rotation Strategy", linewidth=2)
spy_curve.plot(label="SPY", linewidth=2)
plt.title("ETF Momentum Rotation vs SPY")
plt.grid()
plt.legend()
plt.savefig("images/equity_curve.png", dpi=150, bbox_inches="tight")
plt.show()


# Drawdown plot
plt.figure(figsize=(12,4))
strategy_dd.plot(label="Strategy", color="red")
spy_dd.plot(label="SPY", color="blue")
plt.title("Drawdown Comparison")
plt.grid()
plt.legend()
plt.savefig("images/drawdown.png", dpi=150, bbox_inches="tight")
plt.show()

# signal heatmap 
plt.figure(figsize=(10,5))
plt.imshow(signal.tail(120).T, aspect='auto', cmap='coolwarm')
plt.colorbar()
plt.yticks(range(len(signal.columns)), signal.columns)
plt.title("Risk-Adjusted Momentum Signal (Last 120 Days)")
plt.savefig("images/signal.png", dpi=150, bbox_inches="tight")
plt.show()

# weights evolution plot & latest weights
weights.tail(252).plot.area(figsize=(12,5))
plt.title("Portfolio Weights Evolution (Last Year)")
plt.legend(loc="upper left")
plt.savefig("images/weights.png", dpi=150, bbox_inches="tight")
plt.show()

latest_weights = weights.iloc[-1]
print("CURRENT WEIGHTS")
print(latest_weights[latest_weights > 0].sort_values(ascending=False))
