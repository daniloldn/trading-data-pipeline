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

    #path
    Path("data/backtest/metrics").mkdir(parents=True, exist_ok=True)
    Path("data/backtest/timeseries").mkdir(parents=True, exist_ok=True)

    #loading data and 
    for ticker in tickers:
        #setting up position 
        df = pd.read_parquet(f"data/features/{ticker}.parquet")
        df["signal"] =  (df["momentum"] > 1).astype(int)
        df["position"] = df["signal"].shift(1).fillna(0)
        df["strategy_returns"] = df["position"] * df["returns"]
        df["trade"] = df["position"].diff().abs().fillna(0)
        cost_per_trade = 0.001  # 0.1%
        df["strategy_returns_net"] = df["strategy_returns"] - df["trade"] * cost_per_trade

        #metrics:
        df["equity"] = (1 + df["strategy_returns_net"]).cumprod()
        total_return = df["equity"].iloc[-1] - 1
        vol = df["strategy_returns_net"].std() * (252 ** 0.5)
        sharpe = (df["strategy_returns_net"].mean() * 252) / (df["strategy_returns_net"].std() * (252 ** 0.5))
        num_trades = df["trade"].sum()
        #dropdown
        rolling_peak = df["equity"].cummax()
        drawdown = df["equity"] / rolling_peak - 1
        max_dd = drawdown.min()

        #saving 
        final_dict = {"total_returns": total_return,
                   "volatility": vol, 
                   "sharpe": sharpe,
                   "num_trades": num_trades, 
                   "max_drawdown": max_dd}
        final = pd.DataFrame([final_dict])
        #metrics
        final.to_parquet(f"data/backtest/metrics/{ticker}_metrics.parquet")

        #timeseries
        df["drawdown"] = drawdown
        keep = ["Close", "returns", "momentum", "signal", "position", "strategy_returns_net", "equity", "drawdown"]
        df[keep].to_parquet(f"data/backtest/timeseries/{ticker}_timeseries.parquet")

if __name__ == "__main__":
    main()
  
