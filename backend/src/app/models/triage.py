from pydantic import BaseModel, Field
from typing import List, Optional

class TriageCreate(BaseModel):
    """Contrato para criar uma nova triagem."""
    patient_name: str = Field(..., description="Nome completo do paciente", example="João Silva")
    symptoms: List[str] = Field(
        ..., 
        min_length=1, 
        description="Lista de sintomas recolhidos pela enfermeira",
        example=["Febre alta", "Tosse seca", "Dores no corpo"]
    )
    
    
class TriageResponse(BaseModel):
    """Contrato do que o Frontend recebe de volta."""
    id: str
    patient_name: str
    status: str # IN_PROGRESS, SAFETY_PASSED, BLOCKED_EMERGENCY, COMPLETED
    
    # Detalhes que vão sendo preenchidos pelos Agentes
    initial_symptoms: List[str]
    is_allowed: bool
    safety_observations: Optional[str] = None
    suggested_diagnosis: Optional[str] = None
    medication_warnings: Optional[Dict[str, Any]] = None # Pode ser um JSON complexo
    
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        # ISTO É MAGIA: Diz ao Pydantic para ler diretamente dos teus db_models (SQLAlchemy)
        from_attributes = True
        
        
class AgentUpdate(BaseModel):
    is_allowed: bool
    reason: Optional[str] = None