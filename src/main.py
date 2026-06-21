import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import FORECAST_CSV_PATH, FORECAST_HORIZON_DAYS
from src.data_loader import load_raw_alerts
from src.forecast import evaluate_model, forecast_future
from src.preprocess import build_daily_alert_counts, save_processed_series
from src.visualize import plot_forecast

def run_pipeline() -> None:
    print("=" * 60)
    print("Air Raid Alert Time Series Forecast")
    print("=" * 60)
    print("\n[1/5] Loading raw alert data...")
    raw_df = load_raw_alerts()
    print(f"      Loaded {len(raw_df):,} alert events.")
    print(f"      Date range: {raw_df['started_at'].min().date()} to {raw_df['started_at'].max().date()}")
    print("\n[2/5] Building daily alert count time series...")
    daily_series = build_daily_alert_counts(raw_df)
    save_processed_series(daily_series)
    print(f"      Time series has {len(daily_series):,} daily data points.")
    print("\n[3/5] Evaluating model accuracy on held-out recent days...")
    metrics = evaluate_model(daily_series)
    print(f"      Mean Absolute Error (MAE):  {metrics['mae']:.2f} alerts/day")
    print(f"      Mean Absolute % Error (MAPE): {metrics['mape']:.1f}%")
    print(f"\n[4/5] Forecasting {FORECAST_HORIZON_DAYS} days into the future...")
    forecast_series = forecast_future(daily_series, FORECAST_HORIZON_DAYS)
    print(forecast_series.round(1).to_string())
    forecast_series.round(1).to_csv(FORECAST_CSV_PATH, header=True)
    print(f"\n[5/5] Generating chart...")
    plot_forecast(daily_series, forecast_series)
    print("\n" + "=" * 60)
    print("Done. Check the outputs/ folder for the chart and CSV.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as exc:
        print(f"\n[ERROR] Pipeline failed: {exc}", file=sys.stderr)
        raise