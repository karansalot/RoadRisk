# Data Sources

| File | Source | Description | Access date |
|---|---|---|---|
| `raw/pa_total.json` | [PennDOT Crash Incident Details, data.pa.gov (dataset `dc5b-gebx`)](https://data.pa.gov/Public-Safety/Crash-Incident-Details-CY-1997-Current-Annual-Cou/dc5b-gebx) | Count of reported crashes per county per year, 2018–2020, pulled via the Socrata SoQL API (`GROUP BY county_name, crash_year`) | 2026-09-13 |
| `raw/pa_speeding.json` | Same dataset | Count of crashes per county per year flagged `Speeding = Yes` or `Speeding Related = Yes` | 2026-09-13 |
| `raw/pa_fatal.json` | Same dataset | Count of crashes per county per year flagged `Fatal = Yes` | 2026-09-13 |
| `raw/pa_county_population_2020.csv` | [2020 U.S. Census, via Wikipedia "List of counties in Pennsylvania"](https://en.wikipedia.org/wiki/List_of_counties_in_Pennsylvania) | 2020 decennial census population for all 67 PA counties, used to normalize crash counts to rates per 100,000 residents | 2026-09-13 |

## Notes and caveats

- The PennDOT dataset on data.pa.gov was last refreshed through **crash year 2020** at the time of pull — 2018–2020 is the most recent complete three-year window available. A production version of this project would refresh against the live feed annually.
- The `Speeding` and `Speeding Related` flags are officer-coded at the scene (PennDOT crash report fields), not telematics-derived. They are a reasonable real-world proxy for "speeding-related risk" but are not the same as telematics speed-event data a live program would use — see `strategy/government_insurer_strategy.md` for how the pilot closes that gap.
- A small number of records (~5) have a null county and were excluded from the county-level rollup.
- Pennsylvania was chosen as the pilot region because PennDOT publishes complete, county-tagged, flag-level crash microdata through a public API — this made it possible to build a real, reproducible county risk ranking rather than a simulated one. The strategy and financial model are written to generalize to any state DOT / insurer partnership with comparable data.
