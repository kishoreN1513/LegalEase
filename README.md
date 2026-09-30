# LegalEase — Futuristic AI Legal Document Generator

Based on the supplied LegalEase project document:
FastAPI backend + Streamlit frontend + Gemini integration + editable preview + TXT/DOCX/PDF export.

## Termux

pkg update -y
pkg install python -y
cd LegalEase_Futuristic
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env

Terminal 1:
uvicorn backend.main:app --host 0.0.0.0 --port 8000

Terminal 2:
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501

Open:
http://127.0.0.1:8501
API docs:
http://127.0.0.1:8000/docs

If GEMINI_API_KEY is empty, the project uses a local fallback generator so the UI and export flow can still be tested.
