"""Generate project figures."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .config import DATA_PROCESSED, EXOG_LOG_COLUMNS, LEVEL_COLUMNS, LOG_COLUMNS, OUTPUT_FIGURES, ensure_directories
from .model import fit_ecm


def plot_level_trends(df: pd.DataFrame) -> None:
    """Plot raw level variables over time."""
    ensure_directories()
    fig, ax = plt.subplots(figsize=(10, 6))
    for col in ["Y", "X2", "X3"]:
        ax.plot(df["year"], df[col], marker="o", label=col)
    ax.set_title("Kweichow Moutai Operating Variables, 2000-2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("100 million CNY")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "01_level_trends.png", dpi=200)
    plt.close(fig)


def plot_log_scatter_matrix(df: pd.DataFrame) -> None:
    """Plot LNY against logged explanatory variables."""
    ensure_directories()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.ravel()
    for ax, col in zip(axes, EXOG_LOG_COLUMNS):
        ax.scatter(df[col], df["LNY"])
        ax.set_xlabel(col)
        ax.set_ylabel("LNY")
        ax.grid(True, alpha=0.3)
    fig.suptitle("Log-level Scatter Plots")
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "02_log_scatter_matrix.png", dpi=200)
    plt.close(fig)


def plot_actual_fitted_ecm(df: pd.DataFrame) -> None:
    """Plot actual and fitted DLNY from the ECM."""
    ensure_directories()
    ecm, long_run, working, model_df = fit_ecm(df)
    model_df = model_df.copy()
    model_df["fitted_DLNY"] = ecm.fittedvalues

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(model_df["year"], model_df["DLNY"], marker="o", label="Actual DLNY")
    ax.plot(model_df["year"], model_df["fitted_DLNY"], marker="s", label="Fitted DLNY")
    ax.set_title("Actual vs Fitted Net Profit Growth in ECM")
    ax.set_xlabel("Year")
    ax.set_ylabel("Delta log net profit")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "03_actual_fitted_ecm.png", dpi=200)
    plt.close(fig)


def plot_ecm_residuals(df: pd.DataFrame) -> None:
    """Plot ECM residuals over time."""
    ensure_directories()
    ecm, long_run, working, model_df = fit_ecm(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(0, linewidth=1)
    ax.plot(model_df["year"], ecm.resid, marker="o")
    ax.set_title("ECM Residuals")
    ax.set_xlabel("Year")
    ax.set_ylabel("Residual")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_FIGURES / "04_ecm_residuals.png", dpi=200)
    plt.close(fig)


def export_figures(df: pd.DataFrame | None = None) -> None:
    """Export all project figures."""
    if df is None:
        df = pd.read_csv(DATA_PROCESSED)
    plot_level_trends(df)
    plot_log_scatter_matrix(df)
    plot_actual_fitted_ecm(df)
    plot_ecm_residuals(df)


def main() -> None:
    export_figures()
    print(f"Saved figures to {OUTPUT_FIGURES}")


if __name__ == "__main__":
    main()
