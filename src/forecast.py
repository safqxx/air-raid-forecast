import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from src.config import EVALUATION_HOLDOUT_DAYS, SEASONAL_PERIOD_DAYS

def _fit_holt_winters(train_series: pd.Series) -> ExponentialSmoothing:
    model = ExponentialSmoothing(
        train_series,
        trend="add",
        seasonal="add",
        seasonal_periods=SEASONAL_PERIOD_DAYS,
        initialization_method="estimated",
    )
    return model.fit()

def evaluate_model(series: pd.Series) -> dict:
    train = series.iloc[: -EVALUATION_HOLDOUT_DAYS]
    actual_holdout = series.iloc[-EVALUATION_HOLDOUT_DAYS:]
    fitted_model = _fit_holt_winters(train)
    predicted_holdout = fitted_model.forecast(EVALUATION_HOLDOUT_DAYS)
    errors = actual_holdout.values - predicted_holdout.values
    mae = float(np.mean(np.abs(errors)))
    nonzero_mask = actual_holdout.values != 0
    mape = float(np.mean(np.abs(errors[nonzero_mask] / actual_holdout.values[nonzero_mask])) * 100) if nonzero_mask.any() else float("nan")
    return {"mae": mae, "mape": mape, "holdout_days": EVALUATION_HOLDOUT_DAYS}

def forecast_future(series: pd.Series, horizon_days: int) -> pd.Series:
    fitted_model = _fit_holt_winters(series)
    forecast_values = fitted_model.forecast(horizon_days).clip(lower=0)
    future_dates = pd.date_range(start=series.index[-1] + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    forecast_values.index = future_dates
    forecast_values.name = "forecasted_alert_count"
    return forecast_values