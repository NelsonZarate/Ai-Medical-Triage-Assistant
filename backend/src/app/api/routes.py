from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.src.app.agents.crew import run_medical_triage
import json

router = APIRouter()

class PatientInput(BaseModel):
    report: str

@router.post("/triage")
async def start_triage(data: PatientInput):
    try:
        result = run_medical_triage(data.report)

        return json.loads(result.raw) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))