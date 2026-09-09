import os
import json
from google import genai
from google.genai import types
from app.schemas import FeasibilityReportResponse
from app.constants import REGIONAL_PPI, BENCHMARK_UNIT_PRICING

# Initialize the client (it will automatically look for GEMINI_API_KEY in your .env)
client = genai.Client()

SYSTEM_PROMPT = """
You are an expert rural business consultant for the ArthSetu project in India.
Your job is to analyze hyper-local market data and provide a strictly grounded, 
realistic feasibility report for micro-entrepreneurs. 
Never invent financial numbers; use ONLY the data provided in the prompt.
"""

def generate_feasibility_report(
    village: str, 
    category: str, 
    project_cost: float, 
    competitors: int,
    population: int,
    market_access: str,
    state: str = "Maharashtra",
    district: str = "Pune"
):

    state_ppi = REGIONAL_PPI.get(state, {}).get(district, REGIONAL_PPI["default"])
    pricing_data = BENCHMARK_UNIT_PRICING.get(category, BENCHMARK_UNIT_PRICING["Dairy Farming"])


    user_prompt = f"""
    Analyze the feasibility for a new {category} business in {village}.
    
    FACTS TO USE:
    - Total Project Cost: Rs {project_cost}
    - Known Competitors in Area: {competitors}
    - Village Population: {population}
    - Nearby Market Access: {market_access}
    
    FINANCIAL GROUNDING RULES:
    - Purchasing Power Index (PPI) for {district}, {state}: {state_ppi}
    - Apply this PPI to adjust standard revenue models.
    - Benchmark Pricing for {category}: Base price Rs {pricing_data['base_price']} per {pricing_data['unit']}.
    - Keep pricing recommendations between Rs {pricing_data['min_price']} and Rs {pricing_data['max_price']}.
    
    Based on these facts, generate the market reach, opportunities, SWOT, threats, and pricing band.
    """

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=FeasibilityReportResponse,
                temperature=0.2, 
            ),
        )
        return response.text
    except Exception as e:
        print(f"[LLM WARNING] Gemini API unavailable ({e}).")
        return "{}"