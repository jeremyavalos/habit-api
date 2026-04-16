from fastapi import FastAPI
from app.api.v1.router import api_router
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API funcionando"}