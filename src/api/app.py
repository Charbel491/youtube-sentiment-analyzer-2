from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.models.schemas import CommentBatch, PredictionResponse, SentimentPrediction
from src.api.utils.model_loader import load_model
import pandas as pd
import time

app = FastAPI(title="YouTube Sentiment API", version="1.0.0")

# CORS pour extension Chrome
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorizer, model = load_model()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict_batch", response_model=PredictionResponse)
def predict_batch(batch: CommentBatch):
    try:
        start = time.time()
        texts = batch.comments
        X = vectorizer.transform(texts)
        preds = model.predict(X)
        probs = model.predict_proba(X).max(axis=1)

        predictions = [
            SentimentPrediction(comment=c, label=int(p), confidence=float(prob))
            for c, p, prob in zip(texts, preds, probs)
        ]

        stats = {
            "total": len(predictions),
            "positive": int((preds == 1).sum()),
            "neutral": int((preds == 0).sum()),
            "negative": int((preds == -1).sum()),
            "inference_time_ms": round((time.time() - start) * 1000, 2)
        }

        return PredictionResponse(predictions=predictions, stats=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))