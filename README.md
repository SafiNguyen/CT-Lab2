# Sentiment Analysis API

## Student information

- **Student:** Nguyễn Hoàng Long
- **Student ID:** 25127411
- **Course:** Computational Thinking

## Overview

This project provides a FastAPI web service that classifies English text as
`POSITIVE` or `NEGATIVE`. It uses the Hugging Face
[distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)
model. The model is loaded lazily on the first `/predict` request.

## Installation

Python 3.10 or newer is recommended. The dependency list pins
`websockets<14` so the project also works with Python 3.10.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the application

```powershell
uvicorn app:app --reload
```

The interactive API documentation is available at
<http://127.0.0.1:8000/docs>. The first prediction downloads the model from
Hugging Face and may take longer than subsequent requests.

## Endpoints

### `GET /`

Returns an introduction:

```json
{
  "name": "Sentiment Analysis API",
  "description": "Classifies English text as POSITIVE or NEGATIVE.",
  "model": "distilbert-base-uncased-finetuned-sst-2-english",
  "docs": "/docs"
}
```

### `GET /health`

Returns `{"status": "ok"}` when the API process is running.

### `POST /predict`

Request:

```json
{"text": "I really enjoyed this course."}
```

Example response:

```json
{
  "model": "distilbert-base-uncased-finetuned-sst-2-english",
  "text": "I really enjoyed this course.",
  "label": "POSITIVE",
  "score": 0.999
}
```

`text` must contain 1 to 5,000 characters. Invalid input returns HTTP 422.
Model loading or inference failures return HTTP 503 with an explanatory
message.

## Test with `requests`

With the server running in another terminal:

```powershell
python test_api.py
```

The script calls `/health` and sends two different prediction inputs.

## Demonstration video

Replace this placeholder with the public demonstration video link:

`[Demo video link](https://example.com/replace-with-your-video)`
