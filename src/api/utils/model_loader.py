import joblib
import os

MODEL_PATH = "./src/models/logistic_model.joblib"
VECTORIZER_PATH = "./src/models/tfidf_vectorizer.joblib"

model = None
vectorizer = None

def load_model():
    global model, vectorizer
    if model is None:
        model = joblib.load(MODEL_PATH)
    if vectorizer is None:
        vectorizer = joblib.load(VECTORIZER_PATH)
    return vectorizer, model