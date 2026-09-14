"""
Unit tests for the risk-ranking logic in analysis/county_risk_analysis.py.
Runs directly against the raw data checked into data/raw/ -- no network access,
no fixtures beyond what's already in the repo.
"""

import os

import pandas as pd
import pytest

from county_risk_analysis import load_counts, RAW

RAW_TOTAL = "pa_total.json"
RAW_POP = "pa_county_population_2020.csv"


def test_load_counts_returns_one_row_per_county():
    df = load_counts(RAW_TOTAL, "total_crashes")
    assert df["county_name"].is_unique
    # PennDOT covers all 67 PA counties; a handful of null-county records were
    # excluded at the source, so this is an upper bound, not an exact count.
    assert 60 <= len(df) <= 67


def test_load_counts_values_are_positive():
    df = load_counts(RAW_TOTAL, "total_crashes")
    assert (df["total_crashes"] > 0).all()


def test_population_file_has_67_counties_with_positive_population():
    pop = pd.read_csv(os.path.join(RAW, RAW_POP))
    assert len(pop) == 67
    assert (pop["population_2020"] > 0).all()
    assert pop["county"].is_unique


def test_population_file_matches_2020_census_total_order_of_magnitude():
    # Sanity check, not a precise assertion: PA's 2020 census population was
    # ~13.0M. If someone fat-fingers a digit in the CSV, this catches it.
    pop = pd.read_csv(os.path.join(RAW, RAW_POP))
    total = pop["population_2020"].sum()
    assert 12_500_000 <= total <= 13_500_000
