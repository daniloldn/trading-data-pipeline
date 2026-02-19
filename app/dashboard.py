import streamlit as st
import pandas as pd 
import subprocess
from pathlib import Path


st.title("Market Data Pipeline Dashboard")


txt_col1, txt_col2 = st.columns(2)

with txt_col1:
    st.markdown("""
## Project Overview
This dashboard presents the results of an end-to-end financial data pipeline 
that ingests market data, performs cleaning and feature engineering, and 
evaluates a systematic trading strategy through backtesting.

The pipeline architecture:
Ingestion → Cleaning → Feature Engineering → Backtesting → Visualization
""")

with txt_col2:
    st.markdown("""
### Momentum-Based Trading Strategy
The strategy implemented is a simple momentum strategy:

- A momentum indicator is calculated as:  
  **Momentum = Price / 20-day Moving Average**
- If Momentum > 1 → Take a long position (buy)
- If Momentum ≤ 1 → Stay in cash (no position)

To avoid lookahead bias, signals are shifted by one period, meaning:
the decision made today is applied to the next day's returns.
""")

#getting tickers
files = list(Path("data/backtest/timeseries").glob("*_timeseries.parquet"))
tickers = [f.stem.replace("_timeseries", "") for f in files]

if not tickers:
    st.warning("No backtest files found yet. Run the pipeline first.")
    st.stop()

#selceting ticker
selected_ticker = st.selectbox("Select Ticker", tickers)

#running pipeline
if st.button("Run Data Pipeline"):
    with st.spinner("Running pipeline..."):
        result = subprocess.run(
            ["python", "run_pipeline.py"],
            capture_output=True,
            text=True
        )
    st.text(result.stdout)
    if result.returncode != 0:
        st.error(result.stderr)
    st.rerun()


#getting the data
series = pd.read_parquet(f"data/backtest/timeseries/{selected_ticker}_timeseries.parquet")
metrics = pd.read_parquet(f"data/backtest/metrics/{selected_ticker}_metrics.parquet")

#performance indicators
st.subheader("Performance Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total return", round(metrics["total_returns"].iloc[0], 4))
    st.metric("Volatility", round(metrics["volatility"].iloc[0], 4))
with col2:
    st.metric("Sharpe Ratio", round(metrics["sharpe"].iloc[0], 4))
    st.metric("Max Drawdown", round(metrics["max_drawdown"].iloc[0], 4))
with col3:
    st.metric("Numbers of trades", metrics["num_trades"])

st.info("""
### What the Metrics Mean
- **Total Return**: Overall percentage gain/loss of the strategy over the backtest period.
- **Volatility**: Annualised standard deviation of strategy returns (risk measure).
- **Sharpe Ratio**: Risk-adjusted return (higher = better risk efficiency).
- **Max Drawdown**: Largest peak-to-trough loss experienced by the strategy.
- **Number of Trades**: Total number of position changes during the backtest.
""")

#timeseries


st.subheader("Equity Curve")
st.line_chart(series["equity"])
st.expander("""
### Equity Curve
The equity curve shows the cumulative performance of the strategy over time,
assuming reinvestment of profits. It represents how $1 invested at the start 
would have grown under the trading strategy.
""")


st.subheader("Drawdown")
st.line_chart(series["drawdown"])
st.expander("""
### Drawdown Analysis
The drawdown chart shows the percentage decline from the strategy's previous peak.
This is a key risk metric used in systematic trading to assess worst-case losses.

Lower drawdowns indicate more stable and risk-controlled performance.
""")

with st.expander("Technical Implementation Details"):
    st.markdown("""
    - Data Source: Yahoo Finance (yfinance API)
                - Limited to start date of 2025-01-01 because of API limit
    - Storage Format: Parquet files (data lake style)
    - Pipeline Orchestration: Modular Python scripts
    - Backtesting Methodology:
        - Vectorised backtesting
        - Transaction costs included (0.1%)
        - Lookahead bias avoided using signal shift
    """)
