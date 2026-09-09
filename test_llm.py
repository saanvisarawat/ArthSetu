from dotenv import load_dotenv
load_dotenv() # This forces Python to read your .env file

from app.services.llm_engine import generate_feasibility_report

print("Connecting to Gemini API...")

# Passing in dummy data to simulate Shivangi's math
json_output = generate_feasibility_report(
    village="Bassi",
    category="Dairy Farming",
    project_cost=1000000.0,
    competitors=4
)

print("\n--- GEMINI JSON RESPONSE ---")
print(json_output)