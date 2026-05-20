from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "message" : "AI Expense Tracker Backend Running"
    }