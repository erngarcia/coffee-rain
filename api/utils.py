import numpy as np
from datetime import datetime
import pandas as pd

def calculate_confidence_interval(model, scaler, last_12_months: np.ndarray, n_iterations: int = 100):   
    """
    Calculates confidence intervals for rainfall predictions using bootstrap sampling.

    Args:
        model: The trained LSTM model
        scaler: The fitted scaler for data normalization
        last_12_months: Array of historical rainfall values
        n_iterations: Number of bootstrap iterations (default: 100)

    Returns:
        tuple: (lower_bound, upper_bound) representing the 95% confidence interval
        """
    predictions = []
    for _ in range(n_iterations):
        noisy_sequence = last_12_months + np.random.normal(0, 0.1, size=last_12_months.shape)
        scaled_noisy = scaler.transform(noisy_sequence.reshape(-1, 1))
        X_noisy = scaled_noisy.reshape(1, len(last_12_months), 1)
        pred_noisy = scaler.inverse_transform(model.predict(X_noisy))[0][0]
        predictions.append(pred_noisy)
    
    ci_lower = float(np.percentile(predictions, 2.5))
    ci_upper = float(np.percentile(predictions, 97.5))
    
    return ci_lower, ci_upper

def get_next_month_date():
    """
    Calculates the date for the next month's prediction.

    Returns:
        str: First day of next month in 'YYYY-MM-DD' format
    """
    return (datetime.now().replace(day=1) + pd.DateOffset(months=1)).strftime('%Y-%m-%d')
