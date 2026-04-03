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

def preprocess_image(image):
    try:
        height, width = image.shape[:2]

        if width > 1000:
            scale = 1000 / width
            image = cv2.resize(image, (int(width * scale), int(height * scale)))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    except Exception as e:
        raise Exception(f"Preprocess error: {str(e)}")
# -------- OCR --------
def ocr_image(image):
    pil_img = Image.fromarray(image)

    # Faster OCR config
    custom_config = r'--oem 3 --psm 6'

    return pytesseract.image_to_string(pil_img, config=custom_config)


# -------- Mistral API --------
@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if not contents:
            return {"error": "Empty file"}

        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "Invalid image format"}

        # Safe preprocessing
        try:
            image = preprocess_image(image)
        except Exception as e:
            return {"error": f"Preprocessing failed: {str(e)}"}

        # OCR
        try:
            text = ocr_image(image)
        except Exception as e:
            return {"error": f"OCR failed: {str(e)}"}

        # LLM processing
        try:
            result = process_cbcs(text)
        except Exception as e:
            return {"error": f"LLM failed: {str(e)}"}

        return {
            "status": "success",
            "ocr_text": text[:500],
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}