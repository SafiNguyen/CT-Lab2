"""FastAPI service for sentiment analysis with a Hugging Face model."""
"""DistilBERT fine-tuned on SST-2."""
import os
from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_ID = os.getenv("MODEL_ID", "distilbert-base-uncased-finetuned-sst-2-english")

app = FastAPI(
    title="Sentiment Analysis API",
    description="Classify English text as positive or negative using Hugging Face.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    """Request body accepted by the prediction endpoint."""

    text: str = Field(..., min_length=1, max_length=5_000, description="English text to classify")


class PredictionResponse(BaseModel):
    """Structured prediction returned by the API."""

    model: str
    text: str
    label: str
    score: float


@lru_cache(maxsize=1)
def get_classifier() -> Any:
    """Load the model once, on the first inference request."""
    from transformers import pipeline

    return pipeline("sentiment-analysis", model=MODEL_ID)


@app.get("/")
def introduction() -> dict[str, str]:
    """Describe the service."""
    return {
        "name": "Sentiment Analysis API",
        "description": "Classifies English text as POSITIVE or NEGATIVE.",
        "model": MODEL_ID,
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the API process is accepting requests."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Run sentiment inference for one piece of text."""
    try:
        result = get_classifier()(request.text)[0]
    except (ImportError, OSError, RuntimeError, ValueError) as exc:
        raise HTTPException(
            status_code=503,
            detail="The sentiment model is unavailable. Check model access and dependencies.",
        ) from exc

    return PredictionResponse(
        model=MODEL_ID,
        text=request.text,
        label=str(result["label"]),
        score=float(result["score"]),
    )
