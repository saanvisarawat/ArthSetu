# Master Business Categories and Risk Matrix for ArthSetu LLM Feasibility Engine

# --- Module 2: Smart Financial Calculator and Scheme Router (Shivangi) ---

# Rs 1.40 Lakh boundary is inclusive to the Micro Finance Scheme (2.2)
PROJECT_COST_SCHEME_BOUNDARY = 140000

# Above this, project cost is outside both scheme caps (2.1 / 2.2)
MAX_PROJECT_COST = 5000000

# Below this, margin capital produces too small a project to be a real
# micro-enterprise (2.1 edge case)
MIN_MARGIN_CAPITAL = 5000

SCHEMES = {
    "micro_finance": {
        "name": "Micro Finance Scheme",
        "interest_rate": 6.5,       # % p.a.
        "tenure_years": 3,
        "moratorium_months": 3,
        "loan_cap": 125000,         # Rs 1.25 Lakh
    },
    "term_loan": {
        "name": "Term Loan Scheme",
        "interest_rate": 8.0,       # % p.a.
        "tenure_years": 7,
        "moratorium_months": 6,
        "loan_cap": 4500000,        # Rs 45 Lakh
    },
}

BUSINESS_CATEGORIES = {
    "dairy_farming": {
        "label": "Dairy & Milk Production",
        "typical_capex_range": [50000, 200000],
        "working_capital_intensity": "High",
        "perishability_risk": "High",
        "seasonal_demand": "Low",
        "supply_chain_bottlenecks": [
            "Cold chain storage absence",
            "Cattle feed price inflation",
            "Veterinary doctor availability"
        ],
        "cash_flow_cycle": "Daily / Weekly (via local dairy co-ops or milk collection centers)"
    },
    "flour_oil_milling": {
        "label": "Small Agro-Processing (Atta / Oil Chakkis)",
        "typical_capex_range": [70000, 250000],
        "working_capital_intensity": "Medium",
        "perishability_risk": "Low",
        "seasonal_demand": "High (Peaks during post-harvest seasons: Rabi/Kharif)",
        "supply_chain_bottlenecks": [
            "Frequent three-phase power outages",
            "Seasonal raw mustard/grain procurement price volatility",
            "Equipment spare parts turnaround time"
        ],
        "cash_flow_cycle": "Immediate cash / processing fee per kg"
    },
    "poultry_broiler": {
        "label": "Poultry Farming (Broiler / Layer)",
        "typical_capex_range": [80000, 300000],
        "working_capital_intensity": "High",
        "perishability_risk": "High",
        "seasonal_demand": "Moderate (Dips during religious and festival fasting periods)",
        "supply_chain_bottlenecks": [
            "Extreme heat mortality in summer months",
            "Day-old chick (DOC) supply dependencies",
            "Disease outbreaks (Bird flu)"
        ],
        "cash_flow_cycle": "Batch cycle (every 40-45 days)"
    },
    "rural_retail_kirana": {
        "label": "Village Kirana & General Store",
        "typical_capex_range": [40000, 150000],
        "working_capital_intensity": "High",
        "perishability_risk": "Low to Moderate",
        "seasonal_demand": "Low (Steady baseline, spikes during local melas/festivals)",
        "supply_chain_bottlenecks": [
            "High transportation cost to restock from tehsil/district wholesale mandi",
            "Informal credit defaults from village customers (Udhar trap)",
            "Wholesaler minimum order quantities"
        ],
        "cash_flow_cycle": "Daily sales with heavy deferred credit"
    },
    "garment_tailoring": {
        "label": "Textile & Custom Tailoring Unit",
        "typical_capex_range": [30000, 100000],
        "working_capital_intensity": "Low",
        "perishability_risk": "None",
        "seasonal_demand": "High (Concentrated around weddings, Diwali, and Eid seasons)",
        "supply_chain_bottlenecks": [
            "Cloth material access from urban hubs",
            "Single-point dependency on skilled manual labour",
            "Electric sewing motor power reliance"
        ],
        "cash_flow_cycle": "Job-work basis (50% upfront, 50% on delivery)"
    }
}