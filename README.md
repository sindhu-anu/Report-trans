# CBCS Report Analyzer

AI-based backend to extract structured data from CBC lab reports.

## Tech Used
- FastAPI
- Tesseract OCR
- Mistral AI

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run server:
python -m uvicorn app:app --reload

## API Endpoint

POST /process

Send image:

import requests

files = {"image": open("report.jpg", "rb")}
res = requests.post("http://127.0.0.1:8000/process", files=files)

print(res.json())

## Output

Returns structured JSON of patient and test data.
