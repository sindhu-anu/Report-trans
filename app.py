import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import pytesseract
from PIL import Image
import requests

# 🔴 SET THIS PATH (VERY IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

API_KEY = "qgA27H5B1ltUlUS5mt19mBktDpbIkuUu"


# -------- OCR --------
def ocr_image(image):
    pil_img = Image.fromarray(image)
    return pytesseract.image_to_string(pil_img)


# -------- Mistral API --------
def process_cbcs(text):
    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "mistral-small",
    "messages": [
        {
            "role": "user",
            "content": (
                "Extract CBCS lab report data.\n"
                "Return ONLY JSON.\n\n"
                f"Text:\n{text[:3000]}"
            )
        }
    ]
}

    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return response.json()


# -------- ROUTE --------
@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()

    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    text = ocr_image(image)
    result = process_cbcs(text)

    return {"result": result}