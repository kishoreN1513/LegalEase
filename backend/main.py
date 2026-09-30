from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="LegalEase API", version="1.0.0")
app.include_router(router)

@app.get("/")
def root():
    return {"status": "online", "service": "LegalEase API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
