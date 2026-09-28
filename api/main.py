from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from api.db import wait_for_db, get_db

@asynccontextmanager
async def lifespan(app):
    wait_for_db(retries = 10, delay = 2)
    yield

app = FastAPI(lifespan=lifespan)

DbSession = Annotated[Session, Depends(get_db)]

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/health/db")
def get_db_health(db: DbSession):
    db.execute(text("SELECT 1"))
    return {"db": "ok"}