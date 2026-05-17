from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import uuid

# Imports do teu projeto
from app.core.settings import settings
from app.models.triage import TriageCreate, AgentUpdate # Teus Schemas Pydantic
from app.database.db_models import TriageTable # Importa a tabela REAL

# 1. Configuração da Engine (O Motor)
DATABASE_URL = (
    f"{settings.database_driver}://"
    f"{settings.database_username}:{settings.database_password}@"
    f"{settings.database_host}:{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TriageDatabaseService:
    """
    Classe de Serviço para gerir a persistência da Triagem Médica.
    """

    def create_triage_session(self, triage: TriageCreate, db: Session) -> str:
        """Inicializa uma nova triagem com os dados da Nurse."""
        try:
            db_triage = TriageTable(
                id=str(uuid.uuid4()),
                patient_name=triage.patient_name,
                initial_symptoms=triage.symptoms,
                status="IN_PROGRESS",
                created_at=datetime.now(timezone.utc)
            )
            db.add(db_triage)
            db.commit()
            db.refresh(db_triage)
            return db_triage.id
        except Exception as e:
            db.rollback()
            raise ValueError(f"Erro ao iniciar triagem: {str(e)}")

    def update_safety_check(self, triage_id: str, is_allowed: bool, reason: str, db: Session):
        """Atualiza os dados de segurança do Safety Agent."""
        try:
            triage = db.get(TriageTable, triage_id)
            if not triage:
                raise ValueError(f"Sessão {triage_id} não encontrada")
            
            triage.is_allowed = is_allowed
            triage.safety_observations = reason # Nome da coluna deve bater com db_models.py
            
            if not is_allowed:
                triage.status = "BLOCKED_EMERGENCY"
            else:
                triage.status = "SAFETY_PASSED"
            
            db.commit()
            return triage
        except Exception as e:
            db.rollback()
            raise ValueError(f"Erro ao atualizar segurança: {str(e)}")

    def save_final_diagnosis(self, triage_id: str, diagnosis_data: dict, db: Session):
        """Consolida o diagnóstico final dos agentes."""
        try:
            triage = db.get(TriageTable, triage_id)
            if not triage:
                raise ValueError("Triagem não encontrada")
                
            triage.suggested_diagnosis = diagnosis_data.get("diagnosis")
            triage.medication_warnings = diagnosis_data.get("warnings")
            triage.status = "COMPLETED"
            triage.completed_at = datetime.now(timezone.utc)
            
            db.commit()
            db.refresh(triage)
            return triage
        except Exception as e:
            db.rollback()
            raise ValueError(f"Erro ao finalizar diagnóstico: {str(e)}")

# Alias para manter o teu padrão de uso
Database = TriageDatabaseService()

# Dependência para as rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()