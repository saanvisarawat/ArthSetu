from .. import constants


class ValidationError(Exception):
    pass


def calculate_financial_structure(margin_capital: float) -> dict:
    
    if not isinstance(margin_capital, (int, float)) or isinstance(margin_capital, bool):
        raise ValidationError("Margin capital must be a number.")

    if margin_capital <= 0:
        raise ValidationError("Margin capital must be a positive number.")

    if margin_capital < constants.MIN_MARGIN_CAPITAL:
        raise ValidationError(
            f"Margin capital is too low (minimum Rs {constants.MIN_MARGIN_CAPITAL:,}). "
            "This would produce a project cost too small to be a real micro-enterprise."
        )

    project_cost = round(margin_capital / 0.10)
    raw_loan_amount = round(0.90 * project_cost)

    return {
        "margin_capital": round(margin_capital),
        "project_cost": project_cost,
        "raw_loan_amount": raw_loan_amount,
        "contribution_breakdown": {
            "your_contribution": round(margin_capital),
            "your_contribution_pct": 10,
            "loan_component": raw_loan_amount,
            "loan_component_pct": 90,
        },
        "out_of_scheme_range": project_cost > constants.MAX_PROJECT_COST,
    }


def select_scheme(project_cost: float, raw_loan_amount: float) -> dict:
    """
    2.2 Scheme Auto-Selection

    Routes to Micro Finance or Term Loan based on Project Cost, and
    caps the loan amount to that scheme's own ceiling if the raw 90%
    figure from 2.1 would exceed it.
    """
    if project_cost > constants.MAX_PROJECT_COST:
        return {
            "scheme_key": None,
            "scheme_name": None,
            "interest_rate": None,
            "tenure_years": None,
            "moratorium_months": None,
            "loan_cap": None,
            "final_loan_amount": None,
            "capping_note": None,
            "out_of_scheme_range": True,
            "message": (
                f"Project cost of Rs {project_cost:,} exceeds the Rs "
                f"{constants.MAX_PROJECT_COST:,} ceiling covered by either scheme. "
                "No scheme could be auto-selected."
            ),
        }

    # Rs 1.40 Lakh boundary is inclusive to Micro Finance
    if project_cost <= constants.PROJECT_COST_SCHEME_BOUNDARY:
        scheme_key = "micro_finance"
    else:
        scheme_key = "term_loan"

    scheme = constants.SCHEMES[scheme_key]

    final_loan_amount = raw_loan_amount
    capping_note = None
    if raw_loan_amount > scheme["loan_cap"]:
        final_loan_amount = scheme["loan_cap"]
        capping_note = (
            f"Your calculated loan eligibility of Rs {raw_loan_amount:,} exceeds "
            f"the {scheme['name']} cap of Rs {scheme['loan_cap']:,}. "
            f"Loan amount has been capped at Rs {scheme['loan_cap']:,}."
        )

    return {
        "scheme_key": scheme_key,
        "scheme_name": scheme["name"],
        "interest_rate": scheme["interest_rate"],
        "tenure_years": scheme["tenure_years"],
        "moratorium_months": scheme["moratorium_months"],
        "loan_cap": scheme["loan_cap"],
        "final_loan_amount": final_loan_amount,
        "capping_note": capping_note,
        "out_of_scheme_range": False,
        "message": None,
    }


def run_eligibility_engine(margin_capital: float) -> dict:
    """
    Orchestrates 2.1 -> 2.2 end to end. This is what the API endpoint
    calls; it's also what Day 2's EMI Generator (2.3) will build on top of.
    """
    structure = calculate_financial_structure(margin_capital)
    scheme_result = select_scheme(structure["project_cost"], structure["raw_loan_amount"])
    return {**structure, **scheme_result}