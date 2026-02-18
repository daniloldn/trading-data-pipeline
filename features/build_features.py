import pandas as pd 
import yaml
from pathlib import Path


#path 
CONFIG_PATH = Path("configs/universe.yaml")

#reading yaml
with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

#geting yaml information 
tickers = cfg["tickers"]

#storing clean data path
Path("data/features").mkdir(parents=True, exist_ok=True)

#loading data and cleaning 
for ticker in tickers:
    df = pd.read_parquet(f"data/raw/{ticker}.parquet")
    df["returns"] = df["Close"].pct_change()
    df["ma_20"] = df["Close"].rolling(window=20).mean()
    df["volatility"] = df["returns"].rolling(20).std()
    df["momentum"] = df["Close"] / df["ma_20"]
    df.to_parquet(f"data/features/{ticker}.parquet")