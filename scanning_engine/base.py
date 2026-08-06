from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional

class ClassificationResult(BaseModel):
    file_id: str
    assigned_tier: str
    confidence_score: float
    matched_rules: List[str]
    engine_used: str

class BaseClassifier(ABC):
    @abstractmethod
    async def classify(self, file_id: str, text_content: str, manual_override: Optional[str] = None) -> ClassificationResult:
        """
        Evaluate text content and return a structured classification result.
        """
        pass