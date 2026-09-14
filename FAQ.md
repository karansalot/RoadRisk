# FAQ

### Is this a real, currently-running program?

No. The crash data is real (pulled live from PennDOT's public API — see [`data/SOURCES.md`](data/SOURCES.md)), and the analysis is real, but the government-insurer telematics program itself is a design exercise: a strategy, market research brief, and financial model written to be handed to a real state DOT and insurer, not a report on a program that already exists.

### Who is this project for?

It's a portfolio case study demonstrating an end-to-end workflow: pull real public data → analyze it to find a real pattern → design a program around that pattern → build a financial model that honestly tests whether the program pencils out. It's meant to be read by anyone evaluating that workflow, technical or not — see the [plain-English overview](README.md) and [glossary](GLOSSARY.md) if you're the latter.

### Why does the financial model show a negative ROI — is that a bug?

No, it's the intended, honest result. At conservative assumptions (a flat 15% discount paid to every enrollee vs. a claims-savings benefit that only shows up where behavior actually changes), the model's `ROI Summary` tab shows the program doesn't fully pay back within 3 years. This is a well-documented, real dynamic in usage-based-insurance programs — see the note on that tab and in [`strategy/government_insurer_strategy.md`](strategy/government_insurer_strategy.md) for what would close the gap (a score-tiered discount, a longer time horizon, or a second insurer joining the pilot). A version of this model that quietly made the numbers work out would be less trustworthy, not more.

### Is the underlying crash data real, or simulated for this project?

Real. It's pulled directly from [data.pa.gov](https://data.pa.gov)'s public Socrata API (PennDOT's "Crash Incident Details" dataset) and joined with 2020 U.S. Census county population figures. Nothing in `data/raw/` was invented — see [`data/SOURCES.md`](data/SOURCES.md) for exact dataset IDs, access dates, and caveats (e.g., the public dataset's most recent complete year at the time of pull was 2020).

### Can I reuse this for my own state or a different dataset?

Yes — it's MIT-licensed (see [`LICENSE`](LICENSE)). The analysis script (`analysis/county_risk_analysis.py`) expects county-level crash counts with a speeding flag and a fatal flag, plus a population file; swap those inputs for another state's equivalent open-data crash dataset and the ranking, charts, and financial model all still work off the same structure.

### What's the tech stack?

Python (pandas for data wrangling, matplotlib for charts, openpyxl for the Excel model with live formulas), pytest for tests, and GitHub Actions for CI. No paid APIs, databases, or hosted services — everything runs from static files already checked into the repo. See the "Engineering notes" section in the [README](README.md#engineering-notes).

### How do I run this myself?

```bash
python3 -m pip install -r requirements.txt
python3 analysis/county_risk_analysis.py
python3 analysis/build_visuals.py
cd financial_model && python3 build_model.py && cd ..
python3 -m pytest tests/ -v
```

Full details are in the README's [Reproducing everything](README.md#reproducing-everything) section.

### Does running any of this cost money or expose my data?

No. Every script only reads files already in the repo and writes local output files — none of them make network calls, call a paid API, or send data anywhere. The one GitHub Actions workflow (`.github/workflows/tests.yml`) runs tests on push and is free for public repositories, with no schedule that would run it unprompted.
