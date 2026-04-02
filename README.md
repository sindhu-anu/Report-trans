🧪 CBCS Report Analyzer (FastAPI + OCR + AI)

An AI-powered backend system that extracts structured data from CBC (Complete Blood Count) lab reports.

This project processes medical report images and converts them into clean, structured JSON using OCR and AI.

---

## 🚀 Features

- 📤 Upload CBC report images
- 🔍 Extract text using Tesseract OCR
- 🤖 Process data using Mistral AI
- 📊 Convert unstructured data into structured JSON
- ⚡ FastAPI-based backend for real-time processing

---

## 🧠 Tech Stack

- **FastAPI** – Backend framework
- **OpenCV** – Image processing
- **pytesseract** – OCR (text extraction)
- **Mistral AI API** – Data structuring
- **Python** – Core programming language

---

## 📂 Project Structure


.
├── app.py # Main FastAPI backend
├── requirements.txt # Python dependencies
├── render.yaml # Deployment config (Render)
├── apt.txt # System dependencies (Tesseract)
├── .gitignore # Ignored files
├── README.md # Project documentation


---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Install Tesseract OCR

Download from:
https://github.com/UB-Mannheim/tesseract/wiki

If needed, set path in code:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
4️⃣ Set Environment Variable

Create environment variable:

MISTRAL_API_KEY=your_api_key_here
5️⃣ Run the Server
python -m uvicorn app:app --reload
🌐 API Usage
Endpoint:
POST /process
