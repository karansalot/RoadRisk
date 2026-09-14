# Contributing

RoadRisk is primarily a personal portfolio case study, not a project actively seeking contributors — but issues and pull requests are genuinely welcome, especially if you spot a data error, a broken formula, or a way to extend the analysis to another state.

## Reporting a problem

Open an issue using the appropriate template under **Issues → New Issue**. Useful things to include:

- Which file/tab/section is affected
- What you expected vs. what you saw
- If it's a data issue: the specific number and what it should be, ideally with a source

## Suggesting a change

1. Fork the repo and create a branch off `main`.
2. Make your change.
3. If you touched `analysis/county_risk_analysis.py` or the data in `data/raw/`, regenerate the processed outputs so they stay in sync:
   ```bash
   python3 -m pip install -r requirements.txt
   python3 analysis/county_risk_analysis.py
   python3 analysis/build_visuals.py
   ```
4. Run the test suite and make sure it passes:
   ```bash
   python3 -m pytest tests/ -v
   ```
5. If you touched the financial model, rebuild it rather than hand-editing the `.xlsx`:
   ```bash
   cd financial_model && python3 build_model.py
   ```
6. Open a pull request describing what changed and why.

## Conventions this repo follows

- **No hardcoded results in the Excel model.** Every number in `RoadRisk_Financial_Model.xlsx` should be a formula (`=...`), not a value typed in by hand, so the workbook still recalculates correctly if an assumption changes. See `financial_model/build_model.py`.
- **Every assumption is sourced or labeled as an estimate.** If you add a new assumption cell, add a cell comment saying where the number came from, or that it's a program-design estimate — see the existing cells for the pattern.
- **Derived files are generated, not hand-edited.** Everything in `data/processed/` and `analysis/figures/` is produced by a script from the raw data in `data/raw/`. If a number there looks wrong, fix it upstream (the raw data or the script), then regenerate — don't edit the CSV or PNG directly.
- **Tests should fail loudly on a real regression**, not just pass by construction. See `tests/test_outputs.py` for the pattern (checking counts, ranges, and known results, not just "did it run").

## Code style

Standard Python (PEP 8-ish), no linter enforced. Keep functions small and prefer clear variable names over comments — see the existing scripts for the general style.
