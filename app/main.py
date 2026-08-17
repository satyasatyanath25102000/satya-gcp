from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "AI inference API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
