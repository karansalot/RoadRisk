# Market Research Brief: Telematics-Enabled Safe-Driving Programs

*RoadRisk program design series — prepared to support a state DOT / insurer pilot targeting speeding-related crashes and vehicle emissions.*

## 1. Why now

Speeding is a documented and worsening driver of crash severity. NHTSA attributes roughly a **third of all traffic fatalities nationally** to speeding-related crashes, and the [county analysis in this repo](../data/processed/county_risk_scores.csv) shows the same pattern at the state level: several Pennsylvania counties see speeding-related crash rates 5–8x the statewide average, concentrated on rural, higher-speed-limit roads where enforcement density is lowest. At the same time:

- **Telematics hardware and app-based sensing have gotten cheap.** Smartphone-only telematics (accelerometer + GPS, no dongle) now match dedicated OBD-II devices on speed and hard-braking event detection, collapsing the historical cost barrier to scoring a large population of drivers.
- **Insurers already have the incentive infrastructure.** Usage-based insurance (UBI) programs are mainstream, not experimental — the mechanism (discount tied to observed driving behavior) is proven; what's underdeveloped is a **public-sector partner co-funding enrollment in the highest-risk geographies**, where private insurers alone under-invest because loss-ratio improvement in low-density rural counties doesn't move their book enough to justify acquisition spend.
- **States have a budget line this fits.** Highway safety offices (funded via NHTSA Section 402/405 formula grants) already run behavioral safety campaigns (seatbelt, impaired driving, speed enforcement waves). A telematics incentive pilot is a natural extension of that budget rather than new appropriation.

## 2. Competitive / comparable landscape

| Player | Model | Relevant to this program |
|---|---|---|
| **Progressive Snapshot, State Farm Drive Safe & Save, Allstate Drivewise** | Insurer-run UBI, opt-in app or dongle, premium discount based on braking/speed/phone-use score | Proves consumer willingness to trade data for discount; none specifically target *government-designated high-risk counties* — enrollment follows existing policyholder geography, not risk-need geography |
| **Root Insurance** | Telematics-first underwriting (price is *set* by a driving-behavior test period, not adjusted after) | Shows telematics can be the primary rating factor, not just a discount bolt-on — relevant if the state wants an insurer partner willing to go further than a bolt-on discount |
| **Samsara, Geotab, Lytx, Motive** | Commercial fleet telematics + safety coaching, sold to fleet operators (not individual consumers) | Different buyer (B2B fleet), but the coaching/scorecard/gamification mechanics are the most mature in the industry and are directly transferable to a consumer clean-driving incentive design |
| **State-run programs (e.g., Ohio's OhioMeansJobs safety grants, various state "Toward Zero Deaths" coalitions)** | Public safety campaigns, sometimes with local insurer co-marketing | Precedent for state DOT co-branding a private product; usually lack a shared financial mechanism (this program's insurer premium-discount-sharing structure is the gap they don't close) |

**Gap this program fills:** no existing program combines (a) state-directed targeting of the highest-risk counties using DOT crash data, (b) an insurer discount as the enrollment incentive, and (c) a shared KPI/financial structure where the state's cost is offset by measurable reductions in crash-response and infrastructure costs, and the insurer's cost is offset by improved loss ratio in a book segment it wouldn't otherwise prioritize.

## 3. Target population and sizing (Pennsylvania pilot)

Using the risk ranking in [`county_risk_scores.csv`](../data/processed/county_risk_scores.csv), two candidate tiers emerge:

- **Severity tier** (highest per-capita speeding-crash rate, population <100K): Wyoming, Sullivan, Potter, Wayne, Fulton, Warren, Snyder, Susquehanna, Greene, Carbon counties. Highest safety upside per enrolled driver, but small combined insured population (~330K residents) limits the premium pool an insurer partner can discount against.
- **Scale tier** (elevated risk, population >100K): Monroe, Fayette, Dauphin, York, Mercer, Lebanon, Franklin, Lackawanna, Lehigh, Lycoming counties. Lower per-capita rate but far larger insured base (~2.18M residents), giving an insurer partner a commercially meaningful book to price against.

**Recommendation:** launch the Year 1 pilot in the **scale tier**, where enrollment volume makes the insurer's actuarial signal credible within 12 months, and use severity-tier counties as the Year 2 expansion once the discount mechanism and data pipeline are proven — see [`government_insurer_strategy.md`](government_insurer_strategy.md) for the full phasing rationale.

## 4. Willingness to participate — what the research says

Industry telematics adoption studies (J.D. Power UBI studies, insurer-published enrollment data) consistently show:

- **15–20% discount is the threshold** where opt-in rates clear 25–30% of an offered population in the first enrollment year; below ~10% discount, opt-in typically stays under 10%.
- **Privacy concerns are the top stated objection** (cited by ~40% of non-adopters), ahead of "don't want to be monitored" and "not enough discount." A state-co-branded program, positioned as a safety initiative rather than a pure insurer product, tests better on trust in comparable public-private pilots.
- **Gamification and real-time feedback (not just the end-of-term discount) materially increase engagement** — this is the strongest evidence for building a clean-driving score/feedback loop into the program rather than a silent background scoring model (see program design in the strategy doc).

## 5. Risks and open questions to validate before scale-up

1. **Regulatory approval timeline** — the insurer partner's UBI discount filing needs state Department of Insurance approval; this is the single largest schedule risk and should be initiated in parallel with, not after, DOT county selection.
2. **Selection bias** — safer drivers self-select into telematics programs; Year 1 KPIs need a matched control group (non-enrolled drivers in the same counties) to isolate the program's effect from this bias, not just a before/after comparison.
3. **Rural connectivity** — smartphone-only telematics needs continuous or near-continuous data connectivity; several severity-tier counties (Potter, Sullivan, Warren) have documented rural cellular coverage gaps that may require a fallback dongle option, adding cost.
