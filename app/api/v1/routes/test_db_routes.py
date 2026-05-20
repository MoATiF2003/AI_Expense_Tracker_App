from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(
    # prefix="/test-db",
    tags=["Test Database"]
)

@router.get("/test-db")
async def test_database_connection(
    db: Session = Depends(get_db) # Tells FastAPI: Run get_db() and inject result here
):
    db.execute(text("Select 1"))
    return {
        "message" : "Database Connection Successful"
    }