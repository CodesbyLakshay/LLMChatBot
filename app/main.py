from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import engine
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from app.database import engine,Base
from app.routers import auth , chat
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def frontend():
    return FileResponse("static/index.html")

app.include_router(auth.router,prefix="/auth", tags=["Authentication"])
app.include_router(chat.router,prefix="/chat", tags=["Chat"])