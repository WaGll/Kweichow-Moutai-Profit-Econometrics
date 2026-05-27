# Econometric Analysis of Kweichow Moutai Net Profit

> A reproducible econometrics project rebuilt from the course report *Net Profit Model and Empirical Analysis of Kweichow Moutai*. The project studies Kweichow Moutai's annual net profit from 2000 to 2023 using operating revenue, operating cost, GDP growth index and CPI. It implements log transformation, ADF unit-root tests, Engle-Granger cointegration and an Error Correction Model (ECM).

This repository is designed as a GitHub-ready empirical econometrics project rather than a static course assignment. It keeps the original Word report and adds reproducible Python and Stata workflows.

## Research Question

Which factors explain the changes in Kweichow Moutai's net profit? Do operating revenue, operating cost and macroeconomic variables have a long-run equilibrium relationship with net profit? If short-run deviations occur, does an error-correction mechanism drive the system back to equilibrium?

## Data

The sample covers 2000-2023 with 24 annual observations. The raw data are stored in:

```text
data/raw/moutai_profit_2000_2023.csv
```

| Raw variable | Model variable | Description | Unit / definition |
|---|---:|---|---|
| `net_profit_y_billion_cny` | `Y` | Net profit | 100 million CNY |
| `operating_revenue_x2_billion_cny` | `X2` | Operating revenue | 100 million CNY |
| `operating_cost_x3_billion_cny` | `X3` | Operating cost | 100 million CNY |
| `gdp_growth_index_x4_prev_year_100` | `X4` | GDP growth index | previous year = 100 |
| `cpi_x5_1978_100` | `X5` | Consumer price index | 1978 = 100 |

The model uses natural logarithms: `LNY`, `LNX2`, `LNX3`, `LNX4`, and `LNX5`. First differences are denoted as `DLNY`, `DLNX2`, `DLNX3`, `DLNX4`, and `DLNX5`.

## Methodology

```text
Data cleaning
  -> log transformation
  -> descriptive statistics and correlation analysis
  -> ADF unit-root tests
  -> long-run OLS regression
  -> Engle-Granger residual-based cointegration test
  -> Error Correction Model
  -> VIF / White / Breusch-Godfrey diagnostics
  -> exported figures and tables
```

Long-run log model:

```math
\ln Y_t = C + \beta_1 \ln X_{2t} + \beta_2 \ln X_{3t} + \beta_3 \ln X_{4t} + \beta_4 \ln X_{5t} + u_t
```

Error Correction Model:

```math
\Delta \ln Y_t = \alpha_0 + \alpha_1 \Delta \ln X_{2t} + \alpha_2 \Delta \ln X_{3t} + \alpha_3 \Delta \ln X_{4t} + \alpha_4 \Delta \ln X_{5t} + \lambda ECM_{t-1} + \varepsilon_t
```

The final ECM reported in the original paper is:

```math
\Delta \ln Y_t = -0.031873 + 1.677150\Delta\ln X_{2t} - 0.481618\Delta\ln X_{3t} + 0.592824\Delta\ln X_{4t} + 0.532925\Delta\ln X_{5t} - 0.619758ECM_{t-1}
```

## Key Findings

- Operating revenue has a significant positive effect on net-profit growth.
- Operating cost has a significant negative effect on net-profit growth.
- The lagged error-correction term is negative and significant, indicating adjustment toward long-run equilibrium.
- GDP growth and CPI are less significant in the short-run ECM, implying that firm-level operating variables explain more of the annual profit changes than macro variables.
- White and Breusch-Godfrey tests do not indicate serious heteroskedasticity or autocorrelation problems in the final ECM.

## Repository Structure

```text
kweichow-moutai-profit-econometrics/
├─ data/raw/                        # raw annual data
├─ data/processed/                  # generated cleaned data
├─ docs/                            # model guide, framework and reproducibility notes
├─ notebooks/                       # educational notebooks
├─ src/                             # Python implementation
├─ stata/                           # Stata implementation
├─ outputs/figures/                 # generated charts
├─ outputs/tables/                  # generated tables
├─ outputs/models/                  # model summaries
├─ report/计量经济学.docx            # original course report
├─ CITATION.cff
├─ README.md
├─ README_EN.md
├─ requirements.txt
└─ LICENSE
```

## Quick Start with Python

```bash
cd kweichow-moutai-profit-econometrics
pip install -r requirements.txt
python -m src.run_all
```

## Run with Stata

Open Stata in the project root and run:

```stata
do stata/master.do
```

## Data Sources

- National Bureau of Statistics of China: GDP growth and CPI.
- Eastmoney Data Center: Kweichow Moutai financial data.
- CNINFO: Kweichow Moutai income statements from 2000 to 2023.

## License

MIT License. This project is for educational and reproducibility purposes only and does not constitute investment advice.
