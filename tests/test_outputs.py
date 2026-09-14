"""
Regression / data-integrity tests against the processed outputs checked into
data/processed/. These catch a bad re-run of the pipeline (e.g., a bug that
drops counties or produces negative rates) before it gets committed.
"""

import os

import pandas as pd
import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, "data", "processed")


@pytest.fixture
def risk_scores():
    return pd.read_csv(os.path.join(PROCESSED, "county_risk_scores.csv"))


def test_all_67_counties_present(risk_scores):
    assert len(risk_scores) == 67
    assert risk_scores["county_name"].is_unique


def test_risk_rank_is_a_complete_1_to_67_sequence(risk_scores):
    assert sorted(risk_scores["risk_rank"]) == list(range(1, 68))


def test_no_negative_or_missing_rates(risk_scores):
    rate_cols = ["speeding_crash_rate_per_100k", "fatal_crash_rate_per_100k",
                 "speeding_share_of_crashes"]
    for col in rate_cols:
        assert risk_scores[col].notna().all(), f"{col} has missing values"
        assert (risk_scores[col] >= 0).all(), f"{col} has a negative rate"


def test_speeding_share_of_crashes_is_a_valid_fraction(risk_scores):
    assert (risk_scores["speeding_share_of_crashes"] <= 1).all()


def test_top_risk_county_is_a_small_rural_county(risk_scores):
    # Regression check tied to the analysis this repo's strategy docs cite --
    # if this ever fails after a legitimate data refresh, update
    # strategy/market_research_brief.md and government_insurer_strategy.md
    # to match, don't just adjust the test.
    top = risk_scores.sort_values("risk_rank").iloc[0]
    assert top["county_name"] == "Wyoming"
    assert top["population_2020"] < 100_000


def test_pilot_shortlists_match_their_stated_population_tier():
    scale = pd.read_csv(os.path.join(PROCESSED, "pilot_shortlist_scale_tier.csv"))
    severity = pd.read_csv(os.path.join(PROCESSED, "pilot_shortlist_severity_tier.csv"))

    assert len(scale) == 10
    assert len(severity) == 10
    assert (scale["population_2020"] >= 100_000).all()
    assert (severity["population_2020"] < 100_000).all()
    # The two tiers should be disjoint -- no county double-counted.
    assert set(scale["county_name"]).isdisjoint(set(severity["county_name"]))
