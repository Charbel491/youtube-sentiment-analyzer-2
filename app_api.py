from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
from pydantic import BaseModel, Field, field_validator

# -----------------------------
# Chargement une fois au démarrage
# -----------------------------
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
model      = joblib.load("models/logistic_model.joblib")

# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI(title="YouTube-Sentiment", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentBatch(BaseModel):
    comments: List[str] = Field(
        description="Liste de commentaires YouTube"
    )
class SentimentPrediction(BaseModel):
    comment: str
    label: int
    confidence: float

class PredictionResponse(BaseModel):
    predictions: List[SentimentPrediction]
    stats: dict

@app.get("/")
def root():
    return {"message": "YouTube Sentiment API – alive & running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict_batch", response_model=PredictionResponse)
def predict_batch(batch: CommentBatch):
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
    }
    return PredictionResponse(predictions=predictions, stats=stats)