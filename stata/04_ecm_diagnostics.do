/********************************************************************
 04_ecm_diagnostics.do
 Error Correction Model and diagnostic tests.
********************************************************************/

use "data/processed/moutai_profit_with_ecm_stata.dta", clear

display "=== Error Correction Model ==="
reg dlny dlnx2 dlnx3 dlnx4 dlnx5 L.ecm
estimates store ECM

display "=== VIF multicollinearity test ==="
vif

display "=== White heteroskedasticity test ==="
estat imtest, white

display "=== Breusch-Godfrey LM autocorrelation test ==="
estat bgodfrey, lags(1/2)
