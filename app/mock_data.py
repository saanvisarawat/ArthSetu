import uuid
from datetime import datetime

# 1. Corrected Project Mock (Matches ProjectResponse schema exactly)
MOCK_PROJECT = {
    "id": str(uuid.uuid4()),
    "village": "Bassi",
    "block": "Jaipur",
    "district": "Jaipur",
    "state": "Rajasthan",
    "business_category": "Dairy Farming",
    "margin_capital": 100000.0,
    "project_cost": 1000000.0,
    "loan_amount": 900000.0,
    "scheme_type": "term_loan",
    "created_at": datetime.now().isoformat()
}

# 2. Corrected Feasibility Report Mock (Matches the 6 JSON blocks)
MOCK_FEASIBILITY_REPORT = {
    "project_id": MOCK_PROJECT["id"],
    "status": "Completed",
    "language": "en",
    "market_reach_json": {
        "population_reached": 18400,
        "addressable_spend_inr": 2760000,
        "top_channels": ["Twice-weekly local haat", "Direct-to-door delivery"]
    },
    "opportunity_json": {
        "top_niches": [
            {"niche": "Value-added products (Paneer/Ghee)", "rationale": "High demand, zero existing supply in village."}
        ]
    },
    "swot_json": {
        "strengths": ["Low fixed overhead enables lean setup."],
        "weaknesses": ["Tight initial working capital."],
        "opportunities": ["Unserved paneer market."],
        "threats": ["Cold-chain dependency in unstable power grid."]
    },
    "threats_json": {
        "risks": [
            {"threat": "Summer heat milk spoilage", "mitigation": "Allocate Rs 15,000 for insulated chilling cans."}
        ]
    },
    "competitor_json": {
        "estimated_count": 6,
        "saturation_label": "Medium",
        "confidence": "interpolated"
    },
    "pricing_json": {
        "recommended_band": "Rs 48 - 52 / litre",
        "rationale": "Adjusted for below-average district purchasing power (PPI 0.92x)."
    }
}