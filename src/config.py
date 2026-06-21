from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "alerts_sample.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "daily_alert_counts.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FORECAST_CHART_PATH = OUTPUT_DIR / "forecast_chart.png"
FORECAST_CSV_PATH = OUTPUT_DIR / "forecast_values.csv"

FORECAST_HORIZON_DAYS = 14
SEASONAL_PERIOD_DAYS = 7
EVALUATION_HOLDOUT_DAYS = 14