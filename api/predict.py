"""
This module provides functionality for predicting rainfall using an LSTM model.
It includes a RainfallPredictor class that loads a pre-trained model and makes predictions
based on historical rainfall data.
"""

import tensorflow as tf
import joblib
import json
import numpy as np
from pathlib import Path
from typing import List
from utils import calculate_confidence_interval, get_next_month_date

class RainfallPredictor:
    """
    A class for making rainfall predictions using a pre-trained LSTM model.

    This class handles loading the model, preprocessing input data, and generating
    predictions with confidence intervals.

    Attributes:
        model: A trained tensorflow LSTM model
        scaler: A fitted sklearn scaler for data normalization
        metadata: A dictionary containing model metadata including look_back period
    """

    def __init__(self):
        """
        Initializes the RainfallPredictor by loading the required model and preprocessing components.
        
        Raises:
            RuntimeError: If there's an error loading the model or associated files.
        """
        self._load_model()

    def _load_model(self):
        """
        Loads the LSTM model, scaler, and metadata from disk.

        This private method attempts to load:
        - The trained LSTM model (.keras format)
        - The fitted scaler for data normalization
        - Model metadata containing configuration parameters

        Raises:
            RuntimeError: If any required files cannot be loaded or are missing.
        """
        model_path = Path("api/model")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Looking for model in: {model_path.absolute()}")
        print(f"Model directory exists: {model_path.exists()}")
        print(f"Contents of model directory: {list(model_path.glob('*'))}")
        
        try:
            self.model = tf.keras.models.load_model(model_path / 'rainfall_lstm_model.keras')
            self.scaler = joblib.load(model_path / 'scaler.pkl')
            with open(model_path / 'metadata.json', 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")

    def predict(self, historical_rainfall: List[float]) -> dict:
        """
        Predicts the next month's rainfall based on historical rainfall data.

        Args:
            historical_rainfall: A list of float values representing historical rainfall measurements.
                               The length must match the model's look_back period.

        Returns:
            dict: A dictionary containing:
                - prediction: Predicted rainfall value for the next month
                - confidence_interval: Dict with 'lower' and 'upper' bounds
                - prediction_date: The date for which the prediction is made

        Raises:
            ValueError: If the input length doesn't match the required look_back period
            
        Example:
            >>> predictor = RainfallPredictor()
            >>> result = predictor.predict([100, 120, 80, 90, 110, 95, 85, 75, 120, 130, 95, 85])
            >>> print(result)
            {
                'prediction': 98.45,
                'confidence_interval': {'lower': 85.23, 'upper': 111.67},
                'prediction_date': '2025-05-01'
            }
        """
        if len(historical_rainfall) != self.metadata['look_back']:
            raise ValueError(f"Expected {self.metadata['look_back']} months of data")
        
        input_data = np.array(historical_rainfall)
        scaled_sequence = self.scaler.transform(input_data.reshape(-1, 1))
        X_input = scaled_sequence.reshape(1, self.metadata['look_back'], 1)
        
        # Make prediction
        predicted_scaled = self.model.predict(X_input)
        predicted_value = float(self.scaler.inverse_transform(predicted_scaled)[0][0])
        
        # Calculate confidence interval
        ci_lower, ci_upper = calculate_confidence_interval(
            self.model, 
            self.scaler, 
            input_data
        )
        
        return {
            "prediction": predicted_value,
            "confidence_interval": {
                "lower": ci_lower,
                "upper": ci_upper
            },
            "prediction_date": get_next_month_date()
        }

# Create a singleton instance of the predictor
predictor = RainfallPredictor()
