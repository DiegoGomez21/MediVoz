from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import database, models
from app.modules.health.router import router as health_router
from app.modules.medications.router import router as medications_router
from app.modules.reminders.router import router as reminders_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database.Base.metadata.create_all(bind=database.engine)
    yield


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


def create_app() -> FastAPI:
    app = FastAPI(title="MediVoz API", lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(medications_router)
    app.include_router(reminders_router)
    return app


app = create_app()
