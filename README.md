# Rainfall Prediction API for Costa Rican Coffee Harvest Planning

## Overview

This project provides an API for predicting monthly rainfall in Costa Rica, specifically designed to assist coffee growers in harvest planning. Using historical precipitation data and machine learning (LSTM), the system predicts rainfall patterns that can impact coffee harvesting operations.

## Background

Coffee harvesting in Costa Rica Central Valley typically occurs between October and February. Accurate rainfall predictions during this period are crucial for:

* Optimal harvest planning
* Resource allocation
* Risk management
* Climate change adaptation

## Data Source

This project utilizes the PACS Costa Rican Daily Precipitation Dataset:

> UCAR/NCAR - Earth Observing Laboratory. 2011. PACS: Costa Rican Daily Precipitation Data. Version 1.0. UCAR/NCAR - Earth Observing Laboratory. https://doi.org/10.26023/1Z87-M5N7-XB10. Accessed 07 Mar 2025.

## Project Structure

```
├── api/
│   ├── main.py
│   ├── predict.py
|   └── model/
│       ├── metadata.json
│       ├── rainfall_lstm_model.keras
│       └── scaler.pkl
├── Dockerfile
├── requirements.txt
└── README.md
```

## Features

* Monthly rainfall predictions using LSTM neural networks
* Confidence intervals for predictions
* RESTful API interface
* Dockerized deployment
* Historical data analysis capabilities

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API:
```bash
python api/main.py
```

### Docker Setup

1. Build the container:
```bash
docker build -t rainfall-prediction-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 rainfall-prediction-api
```

## API Usage

### Predict Next Month's Rainfall
```bash
curl -X POST "http://localhost:8000/predict/next-month" \
     -H "Content-Type: application/json" \
     -d '{"historical_rainfall": [100, 120, 80, 90, 110, 95, 85, 75, 120, 130, 95, 85]}'
```

### Sample Response
```json
{
    "prediction": 98.45,
    "confidence_interval": {
        "lower": 85.23,
        "upper": 111.67
    },
    "prediction_date": "2025-05-01"
}
```

## Model Details

* Architecture: LSTM (Long Short-Term Memory)
* Input: 12 months of historical rainfall data
* Output: Predicted rainfall for the next month
* Features: Includes confidence intervals for prediction uncertainty

## Current Status and Future Development

This project is currently focused on rainfall prediction as a crucial first step in a larger system for coffee harvest planning. Future developments will include:

* Integration with coffee phenology data
* Harvest timing recommendations
* Climate change impact analysis
* Regional-specific predictions
* Additional agricultural parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License

## Acknowledgments

* UCAR/NCAR Earth Observing Laboratory for providing the precipitation dataset
* Costa Rican coffee growing community for domain expertise
* Fidel my dog for inspo

## Citation

If you use this project in your research, please cite:

```
UCAR/NCAR - Earth Observing Laboratory. 2011. PACS: Costa Rican Daily Precipitation Data. 
Version 1.0. UCAR/NCAR - Earth Observing Laboratory. 
https://doi.org/10.26023/1Z87-M5N7-XB10.
```

## Project Status

- [x] Rainfall prediction model
- [x] API development
- [x] Docker containerization
- [ ] Coffee phenology integration
- [ ] Harvest timing predictions
- [ ] Climate change impact analysis

---

**Note**: This project is part of ongoing research into climate-smart agriculture and precision farming for coffee production in Costa Rica.
