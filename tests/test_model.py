"""Smoke tests for model estimation and ECM coefficients."""
from __future__ import annotations

import pandas as pd
import pytest

from src.config import EXOG_DIFF_COLUMNS
from src.data_process import load_raw_data, preprocess
from src.model import (
    coefficients_table,
    cointegration_residual_adf,
    fit_ecm,
    fit_long_run_model,
    export_model_outputs,
)


# Expected ECM coefficients from the original report (EViews).
# Python should reproduce these within a tight tolerance.
BENCHMARK_ECM = {
    "DLNX2": 1.6772,
    "DLNX3": -0.4816,
    "ECM_L1": -0.6198,
}


@pytest.fixture(scope="module")
def processed_df() -> pd.DataFrame:
    return preprocess(load_raw_data())


@pytest.fixture(scope="module")
def ecm_fit(processed_df: pd.DataFrame):
    """Fit models once and reuse across tests in this module."""
    return fit_ecm(processed_df)


def test_long_run_model_has_expected_params(ecm_fit) -> None:
    """Long-run model should include constant and 4 log-X variables."""
    _ecm, long_run, _working, _model_df = ecm_fit
    expected_params = {"const", *EXOG_DIFF_COLUMNS}  # same names (no L prefix check)
    # Actually long-run uses LNX2..LNX5, not DLNX.
    from src.config import EXOG_LOG_COLUMNS

    expected = {"const", *EXOG_LOG_COLUMNS}
    params = set(long_run.params.index)
    assert expected == params, f"Expected {expected}, got {params}"


def test_ecm_model_has_expected_params(ecm_fit) -> None:
    """ECM model should include constant, 4 diff vars, and ECM_L1."""
    ecm, _long_run, _working, _model_df = ecm_fit
    expected = {"const", *EXOG_DIFF_COLUMNS, "ECM_L1"}
    params = set(ecm.params.index)
    assert expected == params, f"Expected {expected}, got {params}"


def test_ecm_coefficients_match_benchmark(ecm_fit) -> None:
    """ECM key coefficients should match the original EViews report."""
    ecm, _long_run, _working, _model_df = ecm_fit
    for var, expected in BENCHMARK_ECM.items():
        actual = ecm.params[var]
        assert actual == pytest.approx(expected, abs=2e-3), (
            f"{var}: expected {expected:.4f}, got {actual:.4f}"
        )


def test_ecm_error_correction_coefficient_is_negative(ecm_fit) -> None:
    """ECM_L1 coefficient must be negative (error correction towards equilibrium)."""
    ecm, _long_run, _working, _model_df = ecm_fit
    assert ecm.params["ECM_L1"] < 0, (
        f"ECM_L1 should be negative, got {ecm.params['ECM_L1']:.4f}"
    )


def test_eg_cointegration_residual_is_stationary(ecm_fit) -> None:
    """The long-run residual should pass ADF test (p < 0.05)."""
    _ecm, _long_run, working, _model_df = ecm_fit
    adf = cointegration_residual_adf(working["ECM"])
    assert adf["p_value"].iloc[0] < 0.05, (
        f"Cointegration residual ADF p={adf['p_value'].iloc[0]:.4f}, expected < 0.05"
    )


def test_long_run_model_r_squared_high(ecm_fit) -> None:
    """The log-level long-run model should have very high R² (near 1.0)."""
    _ecm, long_run, _working, _model_df = ecm_fit
    assert long_run.rsquared > 0.99, f"Long-run R² = {long_run.rsquared:.4f}, expected > 0.99"


def test_ecm_model_r_squared_reasonable(ecm_fit) -> None:
    """The ECM should have reasonable explanatory power (R² > 0.85)."""
    ecm, _long_run, _working, _model_df = ecm_fit
    assert ecm.rsquared > 0.85, f"ECM R² = {ecm.rsquared:.4f}, expected > 0.85"


def test_coefficients_table_has_expected_columns(ecm_fit) -> None:
    """The coefficient table should include variable, coef, std_err, t_stat, p_value."""
    ecm, _long_run, _working, _model_df = ecm_fit
    tbl = coefficients_table(ecm)
    expected = {"variable", "coef", "std_error", "t_stat", "p_value", "ci_lower", "ci_upper"}
    assert expected.issubset(set(tbl.columns)), f"Missing: {expected - set(tbl.columns)}"


def test_model_working_data_has_ecm_column(ecm_fit) -> None:
    """The working DataFrame must contain the ECM residual and lag columns."""
    _ecm, _long_run, working, _model_df = ecm_fit
    assert "ECM" in working.columns
    assert "ECM_L1" in working.columns


def test_export_model_outputs_returns_expected_bundle(processed_df) -> None:
    """export_model_outputs should return ecm, long_run, working, model_df."""
    bundle = export_model_outputs(processed_df)
    for key in ("ecm", "long_run", "working", "model_df"):
        assert key in bundle, f"Missing key '{key}' in export_model_outputs return"
        assert bundle[key] is not None, f"Key '{key}' is None"
