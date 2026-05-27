/********************************************************************
 01_data_preparation.do
 Import raw CSV data and create log and first-difference variables.
********************************************************************/

import delimited "data/raw/moutai_profit_2000_2023.csv", clear varnames(1) encoding(UTF-8)

rename net_profit_y_billion_cny y
rename operating_revenue_x2_billion_cny x2
rename operating_cost_x3_billion_cny x3
rename gdp_growth_index_x4_prev_year_100 x4
rename cpi_x5_1978_100 x5

sort year
tsset year

label variable y  "Net profit, 100 million CNY"
label variable x2 "Operating revenue, 100 million CNY"
label variable x3 "Operating cost, 100 million CNY"
label variable x4 "GDP growth index, previous year=100"
label variable x5 "CPI, 1978=100"

gen lny  = ln(y)
gen lnx2 = ln(x2)
gen lnx3 = ln(x3)
gen lnx4 = ln(x4)
gen lnx5 = ln(x5)

gen dlny  = D.lny
gen dlnx2 = D.lnx2
gen dlnx3 = D.lnx3
gen dlnx4 = D.lnx4
gen dlnx5 = D.lnx5

label variable lny  "ln(Net profit)"
label variable lnx2 "ln(Operating revenue)"
label variable lnx3 "ln(Operating cost)"
label variable lnx4 "ln(GDP growth index)"
label variable lnx5 "ln(CPI)"
label variable dlny  "D.ln(Net profit)"
label variable dlnx2 "D.ln(Operating revenue)"
label variable dlnx3 "D.ln(Operating cost)"
label variable dlnx4 "D.ln(GDP growth index)"
label variable dlnx5 "D.ln(CPI)"

save "data/processed/moutai_profit_processed_stata.dta", replace
export delimited using "data/processed/moutai_profit_processed_stata.csv", replace
