from backend.src.app.database.services import Database, SessionLocal
from backend.src.app.models.triage import TriageCreate

# 1. Criar uma sessão manual
db = SessionLocal()

# 2. Mock de dados
mock_data = TriageCreate(patient_name="Nelson", symptoms=["febre", "tosse"])

# 3. Testar inserção
try:
    new_id = Database.create_triage_session(mock_data, db)
    print(f"✅ Sucesso! Triagem criada com ID: {new_id}")
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    db.close()