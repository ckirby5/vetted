from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from api.db import wait_for_db, get_db
from api.es_client import get_es_client, search_eligibility

es_client = get_es_client()

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

@app.get("/search")
def get_search(q: str = Query(..., description="Search keyword(required)"),
    category: str = Query(None, description="Category(optional)"),
    state: str = Query(None, description="State(optional)")
    ):
        if not q or not q.strip():
             raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="The 'q' query parameter cannot be missing or empty"
             )
        results = search_eligibility(es_client, q, category=category, state=state)
        shaped_results = []
        for result in results:
             shaped_results.append({
                "program_name": result["_source"]["program_name"],
                "category": result["_source"]["category"],
                "jurisdiction": result["_source"]["jurisdiction"],
                "state": result["_source"]["state"],
                "raw_text": result["_source"]["raw_text"],
                "source_url": result["_source"]["source_url"],
                "score": result["_score"]
             })
        return {"results": shaped_results, "count": len(results)}
             
