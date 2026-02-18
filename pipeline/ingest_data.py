import yfinance as yf
import pandas as pd
import yaml
from pathlib import Path


def main():
    #path 
    CONFIG_PATH = Path("configs/universe.yaml")

    #reading yaml
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    #geting yaml information 
    tickers = cfg["tickers"]
    start_date = cfg["start_date"]
    frequency = cfg.get("frequency", "1d")


    #storing data path 
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    #downloading data
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, interval=frequency)
        data.to_parquet(f"data/raw/{ticker}.parquet")

    return None

if __name__ == "__main__":
    main()

