from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API running 🚀"}


app.include_router(api_router, prefix="/api/v1")