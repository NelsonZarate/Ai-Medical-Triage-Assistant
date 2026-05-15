from pydantic import BaseModel, Field
from typing import List, Optional

class NurseSummary(BaseModel):
    chief_complaint: str = Field(..., description="The patient's main complaint in a few words.")
    duration: str = Field(..., description="How long the patient has been experiencing the symptoms.")
    pain_level: Optional[int] = Field(None, description="Reported pain level (1 to 10). Null if not reported.")
    secondary_symptoms: List[str] = Field(default_factory=list, description="Additional symptoms described by the patient.")
    red_flags: bool = Field(..., description="True if there are high-risk signs (e.g., severe shortness of breath, crushing chest pain, profuse bleeding).")
    needs_more_info: bool = Field(..., description="True if crucial information is missing, such as the chief complaint or duration.")