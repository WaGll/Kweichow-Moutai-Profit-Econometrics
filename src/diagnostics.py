"""Econometric diagnostic tests used in the project."""
from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller

from .config import (
    DATA_PROCESSED,
    DIFF_COLUMNS,
    EXOG_DIFF_COLUMNS,
    LOG_COLUMNS,
    OUTPUT_TABLES,
    ensure_directories,
)
from .model import fit_ecm


def adf_table(df: pd.DataFrame, columns: list[str], regression: str = "c") -> pd.DataFrame:
    """Return ADF results for selected columns.

    regression='c' includes a constant. This is a transparent default for Python
    reproduction. Researchers can change it to 'ct' or 'n' for robustness.
    """
    rows = []
    for col in columns:
        series = df[col].dropna()
        stat, pvalue, lags, nobs, critical_values, icbest = adfuller(
            series, regression=regression, autolag="AIC"
        )
        rows.append(
            {
                "variable": col,
                "regression": regression,
                "adf_stat": stat,
                "p_value": pvalue,
                "lags": lags,
                "nobs": nobs,
                "critical_1pct": critical_values.get("1%"),
                "critical_5pct": critical_values.get("5%"),
                "critical_10pct": critical_values.get("10%"),
                "icbest": icbest,
                "stationary_at_5pct": stat < critical_values.get("5%"),
            }
        )
    return pd.DataFrame(rows)


def vif_table(x: pd.DataFrame) -> pd.DataFrame:
    """Compute Variance Inflation Factors."""
    x_const = sm.add_constant(x)
    return pd.DataFrame(
        {
            "variable": x_const.columns,
            "vif": [variance_inflation_factor(x_const.values, i) for i in range(x_const.shape[1])],
        }
    )


def diagnostic_tests(ecm_result) -> pd.DataFrame:
    """Run White heteroskedasticity and Breusch-Godfrey autocorrelation tests."""
    white = het_white(ecm_result.resid, ecm_result.model.exog)
    bg = acorr_breusch_godfrey(ecm_result, nlags=2)
    return pd.DataFrame(
        [
            {
                "test": "White heteroskedasticity test",
                "statistic_type": "LM",
                "statistic": white[0],
                "p_value": white[1],
            },
            {
                "test": "White heteroskedasticity test",
                "statistic_type": "F",
                "statistic": white[2],
                "p_value": white[3],
            },
            {
                "test": "Breusch-Godfrey LM autocorrelation test",
                "statistic_type": "LM",
                "statistic": bg[0],
                "p_value": bg[1],
            },
            {
                "test": "Breusch-Godfrey LM autocorrelation test",
                "statistic_type": "F",
                "statistic": bg[2],
                "p_value": bg[3],
            },
        ]
    )


def export_descriptive_tables(df: pd.DataFrame) -> None:
    """Export descriptive statistics and correlation matrix."""
    ensure_directories()
    stats = df[LOG_COLUMNS].describe().T
    stats = stats.rename(
        columns={"mean": "Mean", "50%": "Median", "max": "Maximum", "min": "Minimum", "std": "Std. Dev.", "count": "Observations"}
    )
    stats[["Mean", "Median", "Maximum", "Minimum", "Std. Dev.", "Observations"]].to_csv(
        OUTPUT_TABLES / "descriptive_statistics.csv", encoding="utf-8-sig"
    )
    df[LOG_COLUMNS].corr().to_csv(OUTPUT_TABLES / "correlation_matrix.csv", encoding="utf-8-sig")


def export_diagnostics(df: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
    """Run and export all diagnostic outputs."""
    ensure_directories()
    if df is None:
        df = pd.read_csv(DATA_PROCESSED)

    export_descriptive_tables(df)
    adf = adf_table(df, [*LOG_COLUMNS, *DIFF_COLUMNS], regression="c")
    adf.to_csv(OUTPUT_TABLES / "adf_tests.csv", index=False, encoding="utf-8-sig")

    ecm, long_run, working, model_df = fit_ecm(df)
    vif = vif_table(model_df[[*EXOG_DIFF_COLUMNS, "ECM_L1"]])
    vif.to_csv(OUTPUT_TABLES / "vif.csv", index=False, encoding="utf-8-sig")

    diag = diagnostic_tests(ecm)
    diag.to_csv(OUTPUT_TABLES / "diagnostic_tests.csv", index=False, encoding="utf-8-sig")

    return {"adf": adf, "vif": vif, "diagnostics": diag}


def main() -> None:
    outputs = export_diagnostics()
    print("=== ADF tests ===")
    print(outputs["adf"].to_string(index=False))
    print("\n=== VIF ===")
    print(outputs["vif"].to_string(index=False))
    print("\n=== Diagnostic tests ===")
    print(outputs["diagnostics"].to_string(index=False))


if __name__ == "__main__":
    main()
