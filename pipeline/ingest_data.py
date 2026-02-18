import yfinance as yf
import pandas as pd
import yaml
from pathlib import Path


#path 
CONFIG_PATH = Path("Configs/universe.yaml")

#reading yaml
with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

#geting yaml information 
tickers = cfg["tickers"]
start_date = cfg["start_date"]
frequency = cfg.get("frequency", "1d")


#downloading data
for ticker in tickers:
    data = yf.download(ticker, start=start_date)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    data.to_parquet(f"data/raw/{ticker}.parquet")





