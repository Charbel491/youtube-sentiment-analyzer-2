from pydantic import BaseModel, Field, field_validator
from typing import List

class CommentBatch(BaseModel):
    comments: List[str] = Field(
        description="Liste de commentaires YouTube"
    )

    # validation de la taille de la liste via un validateur explicite
    @field_validator("comments")
    def check_size(cls, v):
        if len(v) < 1 or len(v) > 100:
            raise ValueError("Le nombre de commentaires doit être entre 1 et 100")
        return v

class SentimentPrediction(BaseModel):
    comment: str
    label: int
    confidence: float

class PredictionResponse(BaseModel):
    predictions: List[SentimentPrediction]
    stats: dict  # répartition des labels