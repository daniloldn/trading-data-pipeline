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
Path("data/clean").mkdir(parents=True, exist_ok=True)

#loading data and cleaning 
for ticker in tickers:
    df = pd.read_parquet(f"data/raw/{ticker}.parquet")
    df = df.drop_duplicates()
    df = df.sort_index()
    df = df.ffill()
    df.to_parquet(f"data/clean/{ticker}.parquet")