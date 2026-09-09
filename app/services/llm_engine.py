import os
from google import genai
from google.genai import types
from app.schemas import FeasibilityReportResponse

# Initialize the client (it will automatically look for GEMINI_API_KEY in your .env)
client = genai.Client()

SYSTEM_PROMPT = """
You are an expert rural business consultant for the ArthSetu project in India.
Your job is to analyze hyper-local market data and provide a strictly grounded, 
realistic feasibility report for micro-entrepreneurs. 
Never invent financial numbers; use ONLY the data provided in the prompt.
"""

def generate_feasibility_report(village: str, category: str, project_cost: float, competitors: int):
    # This is where we "stuff" the brain with Shivangi's math and local data
    user_prompt = f"""
    Analyze the feasibility for a new {category} business in {village}.
    
    FACTS TO USE:
    - Total Project Cost: Rs {project_cost}
    - Known Competitors in Area: {competitors}
    
    Based on these facts, generate the market reach, opportunities, SWOT, threats, and pricing band.
    """

    # Call Gemini and force it to return Priyanshi's exact Pydantic schema
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=FeasibilityReportResponse,
            temperature=0.2, # Keep it low so it doesn't hallucinate
        ),
    )
    
    return response.text