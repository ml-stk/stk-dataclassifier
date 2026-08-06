import re
from typing import Optional
from .base import BaseClassifier, ClassificationResult

class RegexClassifier(BaseClassifier):
    def __init__(self):
        self.rules = {
            "Restricted": [
                re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), 
                re.compile(r'(?i)strictly[-_\s]confidential')
            ],
            "Confidential": [
                re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b') 
            ]
        }

    async def classify(self, file_id: str, text_content: str, manual_override: Optional[str] = None) -> ClassificationResult:
        if manual_override:
            return ClassificationResult(
                file_id=file_id,
                assigned_tier=manual_override,
                confidence_score=1.0,
                matched_rules=["Manual-User-Override"],
                engine_used="User-Input"
            )

        matched_rules = []
        assigned_tier = "Internal"

        for tier, patterns in self.rules.items():
            for pattern in patterns:
                if pattern.search(text_content):
                    matched_rules.append(pattern.pattern)
                    if tier == "Restricted":
                        assigned_tier = "Restricted"
                    elif tier == "Confidential" and assigned_tier != "Restricted":
                        assigned_tier = "Confidential"

        confidence = 0.90 if matched_rules else 0.40
        return ClassificationResult(
            file_id=file_id,
            assigned_tier=assigned_tier,
            confidence_score=confidence,
            matched_rules=matched_rules,
            engine_used="Regex-Rule-Engine"
        )