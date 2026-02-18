from pipeline.ingest_data import main as run_ingest
from pipeline.clean_data import main as run_clean
from features.build_features import main as run_features
from backtest.strategy import main as run_backtest

def main():
    print("Starting data pipeline...")

    print("Step 1: Ingesting data")
    run_ingest()

    print("Step 2: Cleaning data")
    run_clean()

    print("Step 3: Building features")
    run_features()

    print("Step 4: Running backtest")
    run_backtest()

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()