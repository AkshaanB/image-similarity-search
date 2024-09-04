from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def root():
    
    return JSONResponse(
        status_code=200,
        content={"message":"Root of Jira ticket handler."}
    )
