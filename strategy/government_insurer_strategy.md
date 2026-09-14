# Program Strategy: State DOT–Insurer Telematics Safe-Driving Pilot

## 1. Problem statement

The [county risk analysis](../data/processed/county_risk_scores.csv) identifies a concentrated set of Pennsylvania counties where speeding-related crashes occur at 3–8x the statewide per-capita rate. Existing interventions (enforcement waves, signage, seatbelt/impaired-driving campaigns) are broadcast-style and untargeted at the driver level. There is no mechanism today that (a) reaches drivers in exactly these counties, (b) gives them an ongoing incentive to change behavior rather than a one-time fine, and (c) is funded jointly by the two parties who most directly benefit from fewer speeding-related crashes: the state (crash response, infrastructure, public health cost) and the insurer (claims cost).

## 2. Program design

**Structure:** PennDOT's Bureau of Highway Safety and Traffic Engineering co-sponsors a telematics-based safe-driving program with one or more licensed auto insurers operating in the pilot counties. Enrollment is opt-in and free to the driver.

| Component | Description |
|---|---|
| **Telematics** | Smartphone app (primary) capturing speed relative to posted limit, hard-braking/acceleration events, and phone-distraction events, with a dongle fallback offered in low-connectivity rural counties |
| **Clean-driving incentive** | Insurer-funded premium discount (target 10–20%, tiered by driving score) plus a state-funded one-time enrollment incentive (e.g., $25 gift card or DMV fee credit) to overcome the initial opt-in barrier identified in the market research |
| **Feedback loop** | In-app weekly score plus trip-level alerts for hard-braking/speeding events — engagement research shows this materially outperforms a silent, discount-only design |
| **Governance** | Joint steering committee (PennDOT + insurer + an academic or independent evaluator) to own the KPI dashboard and approve any mid-course changes to incentive levels |
| **Data protection** | Raw trip-level GPS/speed data stays with the insurer's existing telematics vendor under its current privacy/consent framework; PennDOT receives only aggregated, county-level KPI metrics — no individual driver data crosses to the state |

## 3. Target geography and phasing

Per the [market research brief](market_research_brief.md), the pilot launches in the **scale tier** — Monroe, Fayette, Dauphin, York, Mercer, Lebanon, Franklin, Lackawanna, Lehigh, and Lycoming counties (combined population ~2.18M) — where enrollment volume is large enough for the insurer to draw an actuarially credible signal within 12 months. The **severity tier** (Wyoming, Sullivan, Potter, Wayne, Fulton, Warren, Snyder, Susquehanna, Greene, and Carbon counties, combined population ~330K, per [`pilot_shortlist_severity_tier.csv`](../data/processed/pilot_shortlist_severity_tier.csv)) — where per-capita risk is highest but the insured population is small — becomes the Year 2 expansion once the enrollment funnel and data pipeline are validated.

## 4. Year-one KPIs

| KPI | Target | Measurement |
|---|---|---|
| **Speeding violations / speeding-related crashes** | **-5%** in pilot counties vs. a matched control group of similar non-pilot counties, year-over-year | PennDOT crash data (`Speeding` / `Speeding Related` flags, the same fields used in the [risk analysis](../analysis/county_risk_analysis.py)), plus in-app speeding-event rate for enrolled drivers as a leading indicator |
| **Emissions** | **-5%** estimated transportation-related CO2 in enrolled-driver miles vs. their own pre-enrollment baseline | Modeled from telematics data: hard-acceleration/deceleration event rate and average speed variance are established proxies for fuel consumption (EPA MOVES-model relationship between speed volatility and fuel efficiency); this is an **estimated**, not directly metered, emissions figure — see the financial model's KPI Dashboard tab for the calculation and its stated confidence caveat |
| **Enrollment** | 12% of eligible policyholders in pilot counties within 12 months | Insurer enrollment records (leading indicator that gates whether the above two KPIs will have a large enough enrolled base to be statistically meaningful) |
| **Retention** | 70% of enrollees still active at month 12 | Insurer telematics platform |

The 5% targets are deliberately conservative relative to insurer-published UBI results (mature single-carrier UBI programs report 10–30% reductions in hard-braking/speeding events *among enrollees*), because the Year 1 KPI is measured at the **county population level**, diluted by the ~88% of drivers who remain unenrolled in Year 1 — see the financial model for the enrollment-to-population-level-effect math.

## 5. Financial mechanism (summary — full model in [`financial_model/`](../financial_model/))

- **State cost:** enrollment incentives, a share of program administration/marketing, and the DOT-side evaluation staff time.
- **Insurer cost:** the premium discount paid to enrollees, telematics platform licensing, and its share of program administration.
- **State benefit:** avoided crash-response and infrastructure-damage cost, valued using PennDOT's published cost-per-crash estimates, applied to the modeled reduction in crashes.
- **Insurer benefit:** improved loss ratio in the enrolled segment (fewer/less severe claims), plus the standard UBI benefit of adverse-selection screening (safer drivers more likely to enroll and stay).
- **Shared metric:** program-level ROI is tracked jointly so the steering committee can see whether the state or the insurer is carrying a disproportionate share of cost relative to benefit, and rebalance the discount/incentive split in Year 2.

**Honest finding from the model:** at conservative base-case assumptions (a flat 15% discount to every enrollee, a 12% relative loss-ratio improvement), the financial model shows the insurer's discount cost is *not* fully offset by claims savings within the 3-year window — a well-documented tension in real UBI programs, where the discount is paid against the full enrolled book while the claims benefit only accrues where behavior actually changes or a safer driver self-selects in. This is a design input, not a flaw to paper over: it argues for (1) a score-tiered discount rather than a flat rate, so the largest discounts go to the drivers who have actually earned them, and (2) treating Year 1–3 as a build phase where the state accepts that its own attributable benefit (avoided emergency-response and infrastructure cost) is the primary near-term return, while the insurer's return compounds over a longer, multi-cohort horizon than 3 years captures. See the ROI Summary tab in the financial model for the full reasoning.

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Regulatory approval delay for the insurer's UBI discount filing | Insurer files with the PA Insurance Department in parallel with county selection, not after; target a pre-approved discount filing already used in another state to shorten review |
| Flat discount doesn't pay back within 3 years (see financial model) | Move to a score-tiered discount schedule (e.g., 5–20% by driving score band, rather than a flat 15%) starting in Year 2, once enough scored driving data exists to tier confidently |
| Low opt-in in Year 1 | State-funded enrollment incentive plus co-branded marketing through DOT/DMV renewal touchpoints, which have far higher reach than an insurer's own marketing channel |
| Selection bias overstating the effect | Matched control-county design (see KPI table); steering committee reviews the control comparison, not just the raw before/after number |
| Rural connectivity gaps in Year 2 severity-tier counties | Dongle fallback option budgeted into the Year 2 financial model as a per-unit hardware cost |
