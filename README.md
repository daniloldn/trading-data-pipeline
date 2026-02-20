# Trading Data Pipeline

An end-to-end data engineering and data science portfolio project that ingests financial market data, cleans and transforms it through a modular pipeline, engineers trading features, backtests a systematic momentum strategy, and surfaces results in an interactive Streamlit dashboard.

---

## Project Overview

```
Ingestion → Cleaning → Feature Engineering → Backtesting → Visualisation
```

Each stage is a self-contained Python module that reads from and writes to a local Parquet-based data lake. The entire pipeline can be run in a single command or triggered from within the dashboard UI.

---

## Architecture

```
trading-data-pipeline/
├── configs/
│   └── universe.yaml          # Ticker universe, date range, frequency
├── pipeline/
│   ├── ingest_data.py         # Downloads OHLCV data via yfinance
│   └── clean_data.py          # Deduplication, sorting, forward-fill
├── features/
│   └── build_features.py      # Returns, moving average, volatility, momentum
├── backtest/
│   └── strategy.py            # Vectorised momentum strategy + performance metrics
├── app/
│   └── dashboard.py           # Streamlit dashboard
├── data/
│   ├── raw/                   # Raw Parquet files from ingestion
│   ├── clean/                 # Cleaned Parquet files
│   ├── features/              # Feature-engineered Parquet files
│   └── backtest/
│       ├── metrics/           # Per-ticker performance metrics
│       └── timeseries/        # Equity curve, drawdown, signals
├── run_pipeline.py            # Orchestrator — runs all four stages in order
└── requirements.txt
```

---

## Pipeline Stages

### 1. Ingestion (`pipeline/ingest_data.py`)
- Reads ticker symbols, start date, and frequency from `configs/universe.yaml`
- Downloads historical OHLCV data using the **yfinance** API
- Persists one Parquet file per ticker under `data/raw/`

### 2. Cleaning (`pipeline/clean_data.py`)
- Removes duplicate rows
- Sorts by date index
- Forward-fills missing values to handle market holidays and gaps
- Writes cleaned files to `data/clean/`

### 3. Feature Engineering (`features/build_features.py`)
Computes four features for each ticker:

| Feature | Description |
|---|---|
| `returns` | Daily percentage change of closing price |
| `ma_20` | 20-day simple moving average of close |
| `volatility` | 20-day rolling standard deviation of returns |
| `momentum` | `Close / ma_20` — the core signal |

Output is stored under `data/features/`.

### 4. Backtesting (`backtest/strategy.py`)
Implements a **vectorised momentum strategy**:

- **Signal**: `momentum > 1` → long (1), otherwise cash (0)
- **Lookahead bias prevention**: signal is shifted forward by one period before applying to returns
- **Transaction costs**: 0.1% applied on every position change

**Performance metrics computed per ticker:**

| Metric | Description |
|---|---|
| Total Return | Cumulative strategy return over the full period |
| Annualised Volatility | Standard deviation of net returns × √252 |
| Sharpe Ratio | Annualised mean net return / annualised volatility |
| Max Drawdown | Largest peak-to-trough decline of the equity curve |
| Number of Trades | Total position changes over the backtest window |

Results are saved to `data/backtest/metrics/` (summary) and `data/backtest/timeseries/` (full time series including equity curve and drawdown).

---

## Dashboard (`app/dashboard.py`)

An interactive **Streamlit** dashboard that:

- Displays a description of the pipeline architecture and strategy logic
- Lets users select any backtested ticker from a dropdown
- Shows a metrics panel (total return, Sharpe, volatility, max drawdown, trade count)
- Renders an **equity curve** and a **drawdown chart**
- Provides a **"Run Data Pipeline"** button to re-run the full pipeline in-place and refresh results

---

## Configuration

Edit `configs/universe.yaml` to change the ticker universe or date range:

```yaml
tickers:
  - TSLA
start_date: "2025-01-01"
frequency: "1d"
```

> **Note:** yfinance free-tier data availability limits historical depth. The `start_date` is set to 2025-01-01 to stay within reliable API limits.

Multiple tickers can be added to the list and the pipeline will process each one independently.

---

## Getting Started

### Prerequisites
- Python 3.10+

### Installation

```bash
git clone https://github.com/your-username/trading-data-pipeline.git
cd trading-data-pipeline
pip install -r requirements.txt
```

### Run the pipeline

```bash
python run_pipeline.py
```

### Launch the dashboard

```bash
streamlit run app/dashboard.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `yfinance` | Market data ingestion |
| `pandas` | Data transformation and vectorised backtesting |
| `pyarrow` / Parquet | Columnar storage (data lake pattern) |
| `pyyaml` | YAML-based configuration |
| `streamlit` | Interactive results dashboard |

---

## Key Design Decisions

- **Config-driven**: the ticker universe and date range are decoupled from code, making the pipeline easy to extend
- **Parquet storage**: columnar format enables fast reads and low disk footprint, mimicking a lightweight data lake
- **Modular stages**: each pipeline step is independently runnable and testable
- **Vectorised backtesting**: avoids slow row-by-row loops; the entire strategy is expressed as pandas operations
- **No lookahead bias**: signals are strictly lagged before being multiplied by returns
