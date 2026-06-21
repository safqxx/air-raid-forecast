import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from src.config import FORECAST_CHART_PATH

def plot_forecast(historical_series: pd.Series, forecast_series: pd.Series, history_days_to_show: int = 90) -> None:
    recent_history = historical_series.tail(history_days_to_show)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(recent_history.index, recent_history.values, label="Historical daily alert count", color="#2c3e50")
    ax.plot(forecast_series.index, forecast_series.values, label="Forecast", color="#e74c3c", linestyle="--", marker="o", markersize=3)
    ax.axvline(x=historical_series.index[-1], color="gray", linestyle=":", linewidth=1)
    ax.set_title("Daily Air Raid Alert Count: Recent History & Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of alerts started")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    FORECAST_CHART_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FORECAST_CHART_PATH, dpi=150)
    plt.close(fig)
    print(f"[visualize] Saved forecast chart to: {FORECAST_CHART_PATH}")