import streamlit as st
import pandas as pd 
import subprocess
from pathlib import Path


st.title("Market Data Pipeline Dashboard")

st.markdown("""
## Project Overview
This dashboard presents the results of an end-to-end financial data pipeline 
that ingests market data, performs cleaning and feature engineering, and 
evaluates a systematic trading strategy through backtesting.

The pipeline architecture:
Ingestion → Cleaning → Feature Engineering → Backtesting → Visualization
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

#timeseries


st.subheader("Equity Curve")
st.line_chart(series["equity"])


st.subheader("Drawdown")
st.line_chart(series["drawdown"])


