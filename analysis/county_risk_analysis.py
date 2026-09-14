"""
RoadRisk: county-level traffic risk analysis.

Loads PennDOT crash data (2018-2020, via data.pa.gov) and 2020 Census population,
computes speeding-related crash rates and fatal crash rates per 100,000 residents
by county, and ranks counties to identify pilot candidates for a telematics-based
government-insurer safe-driving program.

Usage: python3 county_risk_analysis.py
Outputs:
  - data/processed/county_risk_scores.csv
  - analysis/figures/top20_speeding_crash_rate.png
  - analysis/figures/risk_vs_population.png
"""

import json
import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")
PROCESSED = os.path.join(BASE, "data", "processed")
FIGURES = os.path.join(BASE, "analysis", "figures")

YEARS = ["2018", "2019", "2020"]


def load_counts(filename, value_col):
    with open(os.path.join(RAW, filename)) as f:
        records = json.load(f)
    df = pd.DataFrame(records)
    df["county_name"] = df["county_name"].str.title()
    df[value_col] = pd.to_numeric(df[value_col])
    grouped = df.groupby("county_name")[value_col].sum().reset_index()
    return grouped


def main():
    total = load_counts("pa_total.json", "total_crashes")
    speeding = load_counts("pa_speeding.json", "speeding_crashes")
    fatal = load_counts("pa_fatal.json", "fatal_crashes")
    pop = pd.read_csv(os.path.join(RAW, "pa_county_population_2020.csv"))
    pop["county"] = pop["county"].str.title()

    df = total.merge(speeding, on="county_name", how="left")
    df = df.merge(fatal, on="county_name", how="left")
    df = df.merge(pop, left_on="county_name", right_on="county", how="left")
    df = df.drop(columns=["county"])
    df[["speeding_crashes", "fatal_crashes"]] = df[["speeding_crashes", "fatal_crashes"]].fillna(0)

    n_years = len(YEARS)
    df["avg_annual_crashes"] = df["total_crashes"] / n_years
    df["avg_annual_speeding_crashes"] = df["speeding_crashes"] / n_years
    df["avg_annual_fatal_crashes"] = df["fatal_crashes"] / n_years

    df["speeding_crash_rate_per_100k"] = (
        df["avg_annual_speeding_crashes"] / df["population_2020"] * 100_000
    )
    df["fatal_crash_rate_per_100k"] = (
        df["avg_annual_fatal_crashes"] / df["population_2020"] * 100_000
    )
    df["speeding_share_of_crashes"] = df["speeding_crashes"] / df["total_crashes"]

    # Composite risk score: z-scored blend of speeding-crash rate (exposure to the
    # behavior the program targets) and fatal-crash rate (severity), weighted 60/40.
    for col, z_col in [
        ("speeding_crash_rate_per_100k", "z_speeding_rate"),
        ("fatal_crash_rate_per_100k", "z_fatal_rate"),
    ]:
        df[z_col] = (df[col] - df[col].mean()) / df[col].std()

    df["risk_score"] = 0.6 * df["z_speeding_rate"] + 0.4 * df["z_fatal_rate"]
    df = df.sort_values("risk_score", ascending=False).reset_index(drop=True)
    df["risk_rank"] = df.index + 1

    os.makedirs(PROCESSED, exist_ok=True)
    out_cols = [
        "risk_rank", "county_name", "population_2020",
        "avg_annual_crashes", "avg_annual_speeding_crashes", "avg_annual_fatal_crashes",
        "speeding_crash_rate_per_100k", "fatal_crash_rate_per_100k",
        "speeding_share_of_crashes", "risk_score",
    ]
    df[out_cols].round(3).to_csv(os.path.join(PROCESSED, "county_risk_scores.csv"), index=False)

    top10 = df.head(10)
    print("Top 10 highest-risk PA counties (2018-2020 avg):")
    print(top10[["risk_rank", "county_name", "population_2020",
                  "speeding_crash_rate_per_100k", "fatal_crash_rate_per_100k"]].to_string(index=False))

    # Figure 1: top 20 counties by speeding-related crash rate
    os.makedirs(FIGURES, exist_ok=True)
    top20 = df.head(20).sort_values("speeding_crash_rate_per_100k")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.barh(top20["county_name"], top20["speeding_crash_rate_per_100k"], color="#c0392b")
    ax.set_xlabel("Speeding-related crashes per 100,000 residents (avg/yr, 2018-2020)")
    ax.set_title("Top 20 Highest-Risk PA Counties by Speeding-Related Crash Rate")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "top20_speeding_crash_rate.png"), dpi=150)
    plt.close(fig)

    # Figure 2: risk rate vs population (bubble = total crash volume) to show that
    # risk and population size are not the same thing -- pilot targeting needs both.
    fig, ax = plt.subplots(figsize=(9, 6))
    sizes = df["avg_annual_crashes"] / df["avg_annual_crashes"].max() * 800 + 20
    sc = ax.scatter(
        df["population_2020"], df["speeding_crash_rate_per_100k"],
        s=sizes, alpha=0.6, c=df["risk_score"], cmap="Reds",
    )
    for _, row in df.head(8).iterrows():
        ax.annotate(row["county_name"], (row["population_2020"], row["speeding_crash_rate_per_100k"]),
                    fontsize=8, xytext=(5, 3), textcoords="offset points")
    ax.set_xscale("log")
    ax.set_xlabel("County population (2020, log scale)")
    ax.set_ylabel("Speeding-related crashes per 100,000 residents")
    ax.set_title("County Risk Landscape: Rate vs. Population (bubble size = crash volume)")
    fig.colorbar(sc, label="Composite risk score")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "risk_vs_population.png"), dpi=150)
    plt.close(fig)

    print(f"\nWrote {os.path.join(PROCESSED, 'county_risk_scores.csv')}")
    print(f"Wrote {FIGURES}/top20_speeding_crash_rate.png")
    print(f"Wrote {FIGURES}/risk_vs_population.png")


if __name__ == "__main__":
    main()
