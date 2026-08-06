from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from scanning-engine.regex_worker import RegexClassifier

router = APIRouter(prefix="/api/v1/files", tags=["Classification"])

class ScanRequest(BaseModel):
    file_id: str
    file_name: str
    text_content: str
    manual_override_tier: Optional[str] = None

classifier_engine = RegexClassifier()

@router.post("/classify")
async def classify_file(payload: ScanRequest):
    try:
        result = await classifier_engine.classify(
            file_id=payload.file_id,
            text_content=payload.text_content,
            manual_override=payload.manual_override_tier
        )
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))