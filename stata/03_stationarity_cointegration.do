/********************************************************************
 03_stationarity_cointegration.do
 ADF unit-root tests and Engle-Granger residual-based cointegration test.
********************************************************************/

use "data/processed/moutai_profit_processed_stata.dta", clear

display "=== ADF tests for log-level variables ==="
dfuller lny,  lags(1) trend
dfuller lnx2, lags(1) trend
dfuller lnx3, lags(1) trend
dfuller lnx4, lags(1) trend
dfuller lnx5, lags(1) trend

display "=== ADF tests for first-difference variables ==="
dfuller dlny,  lags(1)
dfuller dlnx2, lags(1)
dfuller dlnx3, lags(1)
dfuller dlnx4, lags(1)
dfuller dlnx5, lags(1)

display "=== Long-run log-level regression ==="
reg lny lnx2 lnx3 lnx4 lnx5
estimates store LONG_RUN
predict ecm, resid
label variable ecm "Residual from long-run log-level regression"

display "=== ADF test on long-run residual for EG cointegration ==="
dfuller ecm, lags(0)

save "data/processed/moutai_profit_with_ecm_stata.dta", replace
