/********************************************************************
 Stata master script
 Kweichow Moutai Net Profit Econometric Analysis
 Data period: 2000-2023
********************************************************************/

do "stata/00_setup.do"
do "stata/01_data_preparation.do"
do "stata/02_descriptive_analysis.do"
do "stata/03_stationarity_cointegration.do"
do "stata/04_ecm_diagnostics.do"
do "stata/05_export_results.do"
