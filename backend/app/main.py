from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.health.router import router as health_router


app = FastAPI(title="MediVoz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
