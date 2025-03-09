from fastapi import FastAPI, HTTPException
from schemas import RainfallInput, RainfallPrediction
from predict import predictor

app = FastAPI(title="Rainfall Prediction API")

@app.get("/")
def home():
    return {
        "message": "Rainfall Prediction API",
        "model_last_trained": predictor.metadata['last_training_date']
    }

@app.post("/predict/next-month", response_model=RainfallPrediction)
def predict_next_month(rainfall_data: RainfallInput):
    try:
        result = predictor.predict(rainfall_data.historical_rainfall)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction error occurred")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
