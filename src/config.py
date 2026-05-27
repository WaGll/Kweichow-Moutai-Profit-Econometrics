"""Project-level path configuration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw" / "moutai_profit_2000_2023.csv"
DATA_PROCESSED = ROOT / "data" / "processed" / "moutai_profit_processed.csv"
OUTPUT_TABLES = ROOT / "outputs" / "tables"
OUTPUT_FIGURES = ROOT / "outputs" / "figures"
OUTPUT_MODELS = ROOT / "outputs" / "models"

RAW_RENAME_MAP = {
    "net_profit_y_billion_cny": "Y",
    "operating_revenue_x2_billion_cny": "X2",
    "operating_cost_x3_billion_cny": "X3",
    "gdp_growth_index_x4_prev_year_100": "X4",
    "cpi_x5_1978_100": "X5",
}

LEVEL_COLUMNS = ["Y", "X2", "X3", "X4", "X5"]
LOG_COLUMNS = ["LNY", "LNX2", "LNX3", "LNX4", "LNX5"]
DIFF_COLUMNS = ["DLNY", "DLNX2", "DLNX3", "DLNX4", "DLNX5"]
EXOG_LOG_COLUMNS = ["LNX2", "LNX3", "LNX4", "LNX5"]
EXOG_DIFF_COLUMNS = ["DLNX2", "DLNX3", "DLNX4", "DLNX5"]


def ensure_directories() -> None:
    """Create output folders if they do not exist."""
    for path in [DATA_PROCESSED.parent, OUTPUT_TABLES, OUTPUT_FIGURES, OUTPUT_MODELS]:
        path.mkdir(parents=True, exist_ok=True)
