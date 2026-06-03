"""Smoke tests for data loading and preprocessing."""
from __future__ import annotations

import numpy as np
import pytest

from src.config import LEVEL_COLUMNS, LOG_COLUMNS, DIFF_COLUMNS, RAW_RENAME_MAP
from src.data_process import load_raw_data, preprocess, save_processed_data


def test_load_raw_data_has_required_columns() -> None:
    """Raw data must contain year and all renamed variable columns."""
    df = load_raw_data()
    required = {"year", *RAW_RENAME_MAP.keys()}
    assert required.issubset(set(df.columns)), f"Missing: {required - set(df.columns)}"
    assert len(df) == 24, f"Expected 24 rows, got {len(df)}"


def test_preprocess_creates_log_and_diff_columns() -> None:
    """Preprocessing must add LN- and DLN- variants for every level column."""
    df = preprocess(load_raw_data())
    for col in LEVEL_COLUMNS:
        assert f"LN{col}" in df.columns, f"Missing LN{col}"
        assert f"DLN{col}" in df.columns, f"Missing DLN{col}"
    assert set(LOG_COLUMNS).issubset(set(df.columns))
    assert set(DIFF_COLUMNS).issubset(set(df.columns))


def test_preprocess_no_null_in_levels_and_logs() -> None:
    """Level and log columns must be fully populated (24 rows)."""
    df = preprocess(load_raw_data())
    for col in [*LEVEL_COLUMNS, *LOG_COLUMNS]:
        assert df[col].notna().all(), f"Column {col} contains nulls"


def test_first_differences_have_one_leading_nan() -> None:
    """First-difference columns should have exactly one NaN in the first row."""
    df = preprocess(load_raw_data())
    for col in DIFF_COLUMNS:
        assert df[col].isna().sum() == 1, f"{col}: expected 1 NaN, got {df[col].isna().sum()}"
        assert df[col].iloc[1:].notna().all(), f"{col}: non-NaN values after row 0"


def test_all_raw_values_positive_for_log() -> None:
    """No level value should be <= 0 (log would be undefined)."""
    df = load_raw_data()
    for col in RAW_RENAME_MAP.keys():
        assert (df[col] > 0).all(), f"Column {col} has non-positive values"


def test_years_are_monotonic() -> None:
    """The dataset is sorted by year in ascending order."""
    df = load_raw_data()
    assert df["year"].is_monotonic_increasing, "Years are not monotonically increasing"


def test_save_processed_data_writes_file(tmp_path) -> None:
    """save_processed_data writes a CSV to the requested path."""
    import src.config as cfg

    original = cfg.DATA_PROCESSED
    try:
        cfg.DATA_PROCESSED = tmp_path / "test_processed.csv"
        df = preprocess(load_raw_data())
        save_processed_data(df, path=cfg.DATA_PROCESSED)
        assert cfg.DATA_PROCESSED.exists()
    finally:
        cfg.DATA_PROCESSED = original
