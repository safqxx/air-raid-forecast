import pandas as pd
from src.config import PROCESSED_DATA_PATH

def build_daily_alert_counts(raw_df: pd.DataFrame) -> pd.Series:
    events = raw_df.copy()
    events["date"] = events["started_at"].dt.date
    oblast_day_pairs = events[["oblast", "date"]].drop_duplicates()
    daily_counts = oblast_day_pairs.groupby("date").size().sort_index()

    full_date_range = pd.date_range(
        start=daily_counts.index.min(),
        end=daily_counts.index.max(),
        freq="D",
    )
    daily_counts.index = pd.to_datetime(daily_counts.index)
    daily_counts = daily_counts.reindex(full_date_range, fill_value=0)
    daily_counts.index.name = "date"
    daily_counts.name = "alert_count"

    last_event_timestamp = raw_df["started_at"].max()
    last_day = daily_counts.index[-1]
    if last_event_timestamp.date() == last_day.date() and last_event_timestamp.hour < 12:
        print(f"[preprocess] Dropping {last_day.date()} -- data cuts off mid-day.")
        daily_counts = daily_counts.iloc[:-1]
    return daily_counts

def save_processed_series(series: pd.Series) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    series.to_csv(PROCESSED_DATA_PATH, header=True)
    print(f"[preprocess] Saved daily time series to: {PROCESSED_DATA_PATH}")