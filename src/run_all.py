"""One-command reproduction pipeline for the full project."""
from __future__ import annotations

from .data_process import main as process_data
from .diagnostics import export_diagnostics
from .model import export_model_outputs
from .visualize import export_figures


def main() -> None:
    print("[1/4] Processing raw data...")
    df = process_data()

    print("[2/4] Estimating long-run model, cointegration residual test and ECM...")
    export_model_outputs(df)

    print("[3/4] Running diagnostic tests and exporting tables...")
    export_diagnostics(df)

    print("[4/4] Exporting figures...")
    export_figures(df)

    print("Done. Results are available in data/processed and outputs/.")


if __name__ == "__main__":
    main()
