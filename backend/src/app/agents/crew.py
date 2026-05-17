from crewai import Crew, Process
from backend.src.app.agents.nurse import triage_nurse, get_triage_task

def run_medical_triage(patient_report: str):

    triage_task = get_triage_task(patient_report)
    

    medical_crew = Crew(
        agents=[triage_nurse],
        tasks=[triage_task],
        process=Process.sequential 
    )
    

    result = medical_crew.kickoff()
    return result