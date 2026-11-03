"""Smoke-test the running API using requests.

Start the server first:
    uvicorn app:app --reload
Then run:
    python test_api.py
"""

import os

import requests

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def check_health() -> None:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    response.raise_for_status()
    assert response.json()["status"] == "ok"


def check_prediction(text: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"text": text},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    assert data["text"] == text
    assert data["label"] in {"POSITIVE", "NEGATIVE"}
    assert 0 <= data["score"] <= 1
    return data


if __name__ == "__main__":
    check_health()
    print(check_prediction("I really enjoyed this course."))
    print(check_prediction("The service was slow and disappointing."))
    print("All API checks passed.")
