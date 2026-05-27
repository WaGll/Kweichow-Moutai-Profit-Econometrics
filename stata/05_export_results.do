/********************************************************************
 05_export_results.do
 Export final Stata working data and close log.
********************************************************************/

capture export delimited using "data/processed/moutai_profit_final_stata.csv", replace
log close

display "Stata workflow completed. See outputs/models/stata_master.log."
