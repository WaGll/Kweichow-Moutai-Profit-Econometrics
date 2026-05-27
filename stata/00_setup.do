/********************************************************************
 00_setup.do
 Project setup for Kweichow Moutai net profit econometric analysis.
 Run from project root through: do stata/master.do
********************************************************************/

clear all
set more off
version 16

capture mkdir "outputs"
capture mkdir "outputs/figures"
capture mkdir "outputs/tables"
capture mkdir "outputs/models"
capture mkdir "data/processed"

capture log close _all
log using "outputs/models/stata_master.log", replace text

display "Project root: `c(pwd)'"
