# ETF Momentum Rotation Strategy
Systematic ETF allocation strategy based on risk-adjusted momentum signals with monthly rebalancing and transaction cost modeling.

### Overview:
The portfolio rotates across multiple ETFs using a combined momentum and volatility signal;
features:
- 60-day momentum
- 20-day volatility scaling
- risk-adjusted scoring (momentum / volatility)
- monthly rebalancing
- fully invested portfolio (long-only)

### ETF Universe

- SPY (US Equity)
- QQQ (Technology)
- EFA (Developed Markets)
- EEM (Emerging Markets)
- TLT (Long Bonds)
- GLD (Gold)

### Methodology

Signal:
Momentum = P / P(60d) - 1  
Volatility = 20d rolling std (annualized)  
Score = Momentum / Volatility  

Portfolio:
- cross-sectional normalization
- weights sum to 1
- lagged by 1 period to avoid look-ahead bias

### Results (20Y Backtest)
- Strategy CAGR ~10.8%
- SPY CAGR ~11.2%
- Strategy Sharpe: higher
- Strategy Drawdown: significantly lower

### Key Insight
The strategy reduces drawdown by dynamically reallocating capital toward lower-risk assets during stress periods, at the cost of slightly lower returns during strong equity bull markets due to momentum lag and diversification effects.

### Strategy Underperformance cases:
The strategy is most vulnerable in the following market regimes:

- **Choppy / mean-reverting markets**, where momentum signals degrade into noise
- **V-shaped recoveries**, where the model exits risk during drawdowns but re-enters after the rebound
- **Low-volatility equity uptrends**, where dispersion across assets is weak and signal strength declines
- **Fast regime shifts**, where the 60-day momentum lookback reacts with delay

In these environments, the strategy may underperform a passive benchmark (SPY) due to lagged signal response and diversification effects.


# How to Run

```bash
pip install -r requirements.txt
python main.py
