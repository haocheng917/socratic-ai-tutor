from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from socratic_ai_tutor.api import auth, membership
from .core.database import engine
from .models import Base
from .api import tutor, upload


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

app.include_router(tutor.router)
app.include_router(upload.router)
app.include_router(auth.router)
app.include_router(membership.router)

@app.get('/')
def root():
    return {"root"}
