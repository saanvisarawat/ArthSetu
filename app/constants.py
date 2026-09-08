# Master Business Categories and Risk Matrix for ArthSetu LLM Feasibility Engine

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