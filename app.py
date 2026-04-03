import pytesseract
from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from PIL import Image
import requests

# 🔴 SET THIS PATH (VERY IMPORTANT)
import platform

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

import os

API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("MISTRAL_API_KEY not set")


# -------- OCR --------
def ocr_image(image):
    pil_img = Image.fromarray(image)

    # Faster OCR config
    custom_config = r'--oem 3 --psm 6'

    return pytesseract.image_to_string(pil_img, config=custom_config)


# -------- Mistral API --------
def process_cbcs(text):
    try:
        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # LIMIT TEXT SIZE (CRITICAL for speed)
        text = text[:2000]

        data = {
            "model": "mistral-small",
            "messages": [
                {
                    "role": "user",
                    "content": f"Extract structured data from this lab report:\n{text}"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=20)

        return response.json()

    except Exception as e:
        return {"error": str(e)}

# -------- ROUTE --------
@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # ✅ ADD THIS (IMPORTANT)
        image = preprocess_image(image)

        text = ocr_image(image)

        result = process_cbcs(text)

        return {
            "status": "success",
            "ocr_text": text[:500],  # preview
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}