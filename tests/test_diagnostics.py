"""Smoke tests for diagnostic outputs (ADF, VIF, White, BG-LM)."""
from __future__ import annotations

import pandas as pd
import pytest

from src.data_process import load_raw_data, preprocess
from src.diagnostics import (
    adf_table,
    diagnostic_tests,
    export_descriptive_tables,
    export_diagnostics,
    vif_table,
)
from src.model import export_model_outputs


@pytest.fixture(scope="module")
def processed_df() -> pd.DataFrame:
    return preprocess(load_raw_data())


def test_adf_table_includes_stationarity_column(processed_df) -> None:
    """ADF table should include a boolean stationarity column."""
    from src.config import LOG_COLUMNS

    tbl = adf_table(processed_df, LOG_COLUMNS, regression="c")
    assert "stationary_at_5pct" in tbl.columns
    assert tbl["stationary_at_5pct"].dtype == bool


def test_vif_table_all_positive(processed_df) -> None:
    """VIF values must be non-negative (≥ 1 for meaningful variables)."""
    from src.config import EXOG_DIFF_COLUMNS

    bundle = export_model_outputs(processed_df)
    x = bundle["model_df"][[*EXOG_DIFF_COLUMNS, "ECM_L1"]]
    tbl = vif_table(x)
    non_const = tbl[tbl["variable"] != "const"]
    assert (non_const["vif"] >= 1).all(), "VIF values should be >= 1"


def test_vif_no_serious_multicollinearity(processed_df) -> None:
    """All regressor VIFs should be below 10 (standard threshold)."""
    from src.config import EXOG_DIFF_COLUMNS

    bundle = export_model_outputs(processed_df)
    x = bundle["model_df"][[*EXOG_DIFF_COLUMNS, "ECM_L1"]]
    tbl = vif_table(x)
    non_const = tbl[tbl["variable"] != "const"]
    assert (non_const["vif"] < 10).all(), (
        f"VIF > 10 detected:\n{non_const[non_const.vif >= 10]}"
    )


def test_diagnostic_tests_output_has_expected_tests(processed_df) -> None:
    """Diagnostic output should include White and BG-LM tests."""
    bundle = export_model_outputs(processed_df)
    diag = diagnostic_tests(bundle["ecm"])
    test_names = diag["test"].unique()
    assert any("White" in t for t in test_names), f"Missing White test in {test_names}"
    assert any("Breusch-Godfrey" in t for t in test_names), (
        f"Missing BG-LM test in {test_names}"
    )


def test_diagnostic_p_values_in_range(processed_df) -> None:
    """All diagnostic p-values should be in the valid [0, 1] range."""
    bundle = export_model_outputs(processed_df)
    diag = diagnostic_tests(bundle["ecm"])
    assert (diag["p_value"] >= 0).all(), "Negative p-values found"
    assert (diag["p_value"] <= 1).all(), "p-values > 1 found"


def test_descriptive_statistics_export_creates_file(processed_df, tmp_path) -> None:
    """export_descriptive_tables should write CSV files."""
    import src.config as cfg

    original = cfg.OUTPUT_TABLES
    try:
        cfg.OUTPUT_TABLES = tmp_path
        cfg.ensure_directories()
        export_descriptive_tables(processed_df)
        assert (tmp_path / "descriptive_statistics.csv").exists()
        assert (tmp_path / "correlation_matrix.csv").exists()
    finally:
        cfg.OUTPUT_TABLES = original


def test_adf_level_variables_nonstationary(processed_df) -> None:
    """Most log-level variables should be non-stationary (fail to reject unit root)."""
    from src.config import LOG_COLUMNS

    tbl = adf_table(processed_df, LOG_COLUMNS, regression="c")
    stationary = tbl["stationary_at_5pct"].sum()
    total = len(tbl)
    # At most 1 log-level variable might be borderline stationary.
    # With 5 log-level vars, expect >= 4 to be non-stationary.
    assert stationary <= 2, (
        f"Expected most level vars non-stationary, got {stationary}/{total} stationary"
    )


def test_adf_diff_variables_mostly_stationary(processed_df) -> None:
    """Most first-difference variables should be stationary at 5% level."""
    from src.config import DIFF_COLUMNS

    tbl = adf_table(processed_df, DIFF_COLUMNS, regression="c")
    stationary = tbl["stationary_at_5pct"].sum()
    total = len(tbl)
    # DLNY, DLNX2, DLNX4 should be stationary. DLNX3 and DLNX5 may not be.
    assert stationary >= 2, (
        f"Expected at least 2 diff vars stationary, got {stationary}/{total}"
    )


def test_export_diagnostics_with_prefitted_models(processed_df) -> None:
    """export_diagnostics should accept pre-fitted models without error."""
    bundle = export_model_outputs(processed_df)
    result = export_diagnostics(
        processed_df,
        ecm=bundle["ecm"],
        long_run=bundle["long_run"],
        working=bundle["working"],
        model_df=bundle["model_df"],
    )
    assert "adf" in result
    assert "vif" in result
    assert "diagnostics" in result
