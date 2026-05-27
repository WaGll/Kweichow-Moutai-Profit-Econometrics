/********************************************************************
 02_descriptive_analysis.do
 Descriptive statistics, correlation analysis and trend chart.
********************************************************************/

use "data/processed/moutai_profit_processed_stata.dta", clear

display "=== Descriptive statistics ==="
summarize lny lnx2 lnx3 lnx4 lnx5

display "=== Correlation matrix ==="
pwcorr lny lnx2 lnx3 lnx4 lnx5, sig star(0.05)

twoway line lny year, title("ln(Net profit), 2000-2023") xtitle("Year") ytitle("LNY")
graph export "outputs/figures/stata_lny_trend.png", replace width(1800)
