from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ClassifyRequest(BaseModel):
    text: str
    filename: Optional[str] = None

class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    reasoning: str

@router.post("/classify", response_model=ClassifyResponse)
async def classify_document(request: ClassifyRequest):
    logger.info(f"Classification request for: {request.filename or 'Unknown'}")
    return ClassifyResponse(
        category="official",
        confidence=0.5,
        reasoning="Placeholder - AI not implemented"
    )

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI router active"}
