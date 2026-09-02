from fastapi import FastAPI
from src.forza_backend.routers import sample

app = FastAPI()

app.include_router(sample.router)