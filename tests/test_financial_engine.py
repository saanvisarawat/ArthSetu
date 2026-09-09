import pytest
from app.services.financial_engine import (
    calculate_financial_structure,
    select_scheme,
    run_eligibility_engine,
    ValidationError,
)


def test_worked_example_1_lakh_capital():
    result = calculate_financial_structure(100000)
    assert result["project_cost"] == 1000000
    assert result["raw_loan_amount"] == 900000
    assert result["contribution_breakdown"]["your_contribution_pct"] == 10
    assert result["contribution_breakdown"]["loan_component_pct"] == 90


def test_rejects_negative_capital():
    with pytest.raises(ValidationError):
        calculate_financial_structure(-5000)


def test_rejects_zero_capital():
    with pytest.raises(ValidationError):
        calculate_financial_structure(0)


def test_rejects_non_numeric_capital():
    with pytest.raises(ValidationError):
        calculate_financial_structure("fifty thousand")


def test_rejects_capital_below_minimum():
    with pytest.raises(ValidationError):
        calculate_financial_structure(2000)


def test_flags_but_does_not_block_out_of_range_project_cost():
    result = calculate_financial_structure(600000)
    assert result["project_cost"] == 6000000
    assert result["out_of_scheme_range"] is True


def test_worked_example_term_loan_no_capping():
    structure = calculate_financial_structure(150000)
    scheme = select_scheme(structure["project_cost"], structure["raw_loan_amount"])
    assert scheme["scheme_key"] == "term_loan"
    assert scheme["final_loan_amount"] == 1350000
    assert scheme["capping_note"] is None


def test_boundary_exactly_1_4_lakh_routes_to_micro_finance():
    scheme = select_scheme(140000, 126000)
    assert scheme["scheme_key"] == "micro_finance"


def test_project_cost_above_50_lakh_is_out_of_range():
    scheme = select_scheme(5100000, 4590000)
    assert scheme["out_of_scheme_range"] is True
    assert scheme["scheme_key"] is None
    assert scheme["message"] is not None


def test_raw_loan_above_micro_finance_cap_is_capped():
    scheme = select_scheme(139000, 125100)
    assert scheme["scheme_key"] == "micro_finance"
    assert scheme["final_loan_amount"] == 125000
    assert scheme["capping_note"] is not None


def test_raw_loan_above_term_loan_cap_is_capped():
    scheme = select_scheme(5000000, 4500001)
    assert scheme["scheme_key"] == "term_loan"
    assert scheme["final_loan_amount"] == 4500000
    assert scheme["capping_note"] is not None


def test_end_to_end_micro_finance_path():
    result = run_eligibility_engine(13900)
    assert result["scheme_key"] == "micro_finance"
    assert result["project_cost"] == 139000


def test_end_to_end_term_loan_path():
    result = run_eligibility_engine(150000)
    assert result["scheme_key"] == "term_loan"
    assert result["final_loan_amount"] == 1350000