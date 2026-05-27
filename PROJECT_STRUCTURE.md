# Project Structure

```text
kweichow-moutai-profit-econometrics/
├─ data/
│  ├─ raw/                         # Raw annual data used by all scripts
│  └─ processed/                   # Generated cleaned/log/differenced data
├─ docs/                           # Methodology, model equations and reproducibility notes
├─ notebooks/                      # Step-by-step classroom notebooks from the original project
├─ src/                            # Python implementation
├─ stata/                          # Stata implementation
├─ outputs/
│  ├─ figures/                     # Generated charts
│  ├─ tables/                      # Generated CSV tables
│  └─ models/                      # Text model summaries and Stata logs
├─ report/                         # Original course report
├─ README.md                       # Chinese project homepage
├─ README_EN.md                    # English project homepage
├─ CITATION.cff                    # Citation metadata
├─ requirements.txt                # Python dependencies
├─ Makefile                        # Optional command shortcuts
└─ LICENSE                         # MIT License
```

## Recommended Workflow

1. Read `report/计量经济学.docx` to understand the original course report.
2. Read `docs/research_framework.md` and `docs/econometric_model_guide.md` for the reconstructed methodology.
3. Run `python -m src.run_all` to reproduce tables and figures.
4. Run `do stata/master.do` in Stata to reproduce the Stata workflow.
