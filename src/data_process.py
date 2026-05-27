"""Data preprocessing for the Kweichow Moutai profit econometrics project.

This script reads the raw annual CSV data, standardizes variable names,
creates natural-log variables and first-difference log variables, then exports
processed data for subsequent modeling.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import DATA_PROCESSED, DATA_RAW, LEVEL_COLUMNS, RAW_RENAME_MAP, ensure_directories


def load_raw_data(path=DATA_RAW) -> pd.DataFrame:
    """Load raw annual data from CSV."""
    df = pd.read_csv(path)
    required_columns = {"year", *RAW_RENAME_MAP.keys()}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in raw data: {sorted(missing)}")
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Rename variables, create log variables and first differences."""
    processed = df.rename(columns=RAW_RENAME_MAP).copy()
    processed = processed.sort_values("year").reset_index(drop=True)

    for col in LEVEL_COLUMNS:
        if (processed[col] <= 0).any():
            raise ValueError(f"Column {col} contains non-positive values and cannot be logged.")
        processed[f"LN{col}"] = np.log(processed[col])
        processed[f"DLN{col}"] = processed[f"LN{col}"].diff()

    return processed


def save_processed_data(df: pd.DataFrame, path=DATA_PROCESSED) -> None:
    """Save processed data to CSV."""
    ensure_directories()
    df.to_csv(path, index=False, encoding="utf-8-sig")


def main() -> pd.DataFrame:
    """Run the full data-processing step."""
    df = preprocess(load_raw_data())
    save_processed_data(df)
    print(f"Saved processed data to {DATA_PROCESSED}")
    return df


if __name__ == "__main__":
    main()
