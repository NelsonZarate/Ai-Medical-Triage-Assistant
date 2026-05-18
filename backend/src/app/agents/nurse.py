# app/agents/nurse.py
import os
from crewai import Agent, Task, LLM
from app.models.schemas import NurseSummary
from dotenv import load_dotenv

load_dotenv() 

triage_llm = LLM(
    model="groq/llama3-70b-8192", 
    api_key=os.getenv("GROQ_API_KEY")
)

triage_nurse = Agent(
    role='First-Line Triage Nurse',
    goal='Extract and structure the patient\'s basic symptoms clearly, objectively, and safely, without ever suggesting diagnoses.',
    backstory="""You are an experienced triage nurse working in a busy emergency department. 
    Your sole function is to listen to the initial complaint, identify the chief complaint, duration, pain level, and any associated symptoms. 
    
    STRICT LIMITS OF YOUR ROLE:
    1. NEVER provide a medical diagnosis.
    2. NEVER suggest treatments, medications, or home remedies.
    3. NEVER attempt to reassure the patient by saying 'it is nothing serious'.
    4. Your focus is 100% on collecting structured data.
    5. If you detect life-threatening symptoms, you must flag the red alert immediately.
    
    Your demeanor is empathetic but highly methodical, scientific, and restrained.""",
    verbose=True,
    allow_delegation=False,
    llm=triage_llm 
)

def get_triage_task(patient_report: str) -> Task:
    return Task(
        description=f"""
        Analyze the following patient report: '{patient_report}'.
        
        Your task is to strictly extract the vital parameters of the patient's complaint and fill out the NurseSummary form.
        
        EXTRACTION RULES AND LIMITS:
        - Ignore emotions, venting, or side stories.
        - Focus ONLY on basic physical symptoms.
        - If the patient does not mention a data point, do not invent. Record it as 'Unknown' or Null.
        - Do not make medical correlations.
        - If the complaint is too vague, set needs_more_info to True.
        """,
        expected_output="A structured summary in JSON strictly following the NurseSummary schema fields.",
        agent=triage_nurse,
        output_json=NurseSummary
    )