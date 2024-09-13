import config
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)

config.setup_logging()

router = APIRouter()

@router.get("/")
async def root():
    logger.info("Request received to the root directory.")

    return JSONResponse(
        status_code=200,
        content={"message":"Root of Image Search."}
    )
