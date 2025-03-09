"""
Schemas for rainfall prediction API request and response models.
"""

from pydantic import BaseModel, validator
from typing import List

class RainfallInput(BaseModel):
    """
    Input schema for rainfall prediction requests.

    Attributes:
        historical_rainfall (List[float]): List of 12 months of historical rainfall values
    """
    historical_rainfall: List[float]

    @validator('historical_rainfall')
    def validate_rainfall_data(cls, v):
        """
        Validates the historical rainfall input data.

        Args:
            v (List[float]): List of rainfall values

        Returns:
            List[float]: Validated list of rainfall values

        Raises:
            ValuzeError: If input length is not 12 or contains negative values
        """
        if len(v) != 12:
            raise ValueError('Must provide exactly 12 months of historical data')
        if any(x < 0 for x in v):
            raise ValueError('Rainfall values cannot be negative')
        return v

class RainfallPrediction(BaseModel):
    """
    Output schema for rainfall predictions.

    Attributes:
        prediction (float): Predicted rainfall value
        confidence_interval (dict): Lower and upper bounds of the prediction
        prediction_date (str): Date for which prediction is made
    """
    prediction: float
    confidence_interval: dict
    prediction_date: str
