import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router

load_dotenv()

app = FastAPI(
    title="Medical Triage AI Assistant",
    description="API for AI-driven first-line medical triage.",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":

    print("Starting Medical Triage API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)