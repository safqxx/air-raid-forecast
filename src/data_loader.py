import pandas as pd
from src.config import RAW_DATA_PATH

REQUIRED_COLUMNS = {"oblast", "started_at", "finished_at"}

def load_raw_alerts() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Could not find raw data file at: {RAW_DATA_PATH}\n"
            "Make sure 'alerts_sample.csv' is present under data/raw/."
        )
    df = pd.read_csv(RAW_DATA_PATH, parse_dates=["started_at", "finished_at"])
    if df.empty:
        raise ValueError(f"The raw data file at {RAW_DATA_PATH} is empty.")
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Raw data file is missing required columns: {missing_columns}.")
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    if len(df) != before:
        print(f"[data_loader] Dropped {before - len(df)} duplicate rows.")
    return df