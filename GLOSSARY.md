# Glossary

Plain-English definitions for the industry and technical terms used throughout this repo, in the order you'd likely hit them.

| Term | What it means here |
|---|---|
| **Speeding-related crash** | A crash where the responding officer marked "speeding" or "speeding-related" as a contributing factor on the police crash report. This is officer-coded at the scene, not measured by a device — see [`data/SOURCES.md`](data/SOURCES.md). |
| **County risk score** | A single number ranking each PA county by how dangerous its speeding-related crash activity is, combining the speeding-crash rate and the fatal-crash rate. Higher = higher priority for the program. See [`analysis/county_risk_analysis.py`](analysis/county_risk_analysis.py). |
| **Per-100,000 residents (per-capita rate)** | A way of comparing counties fairly regardless of size — "how many crashes would happen if this county had exactly 100,000 people," so a small rural county and a big city can be compared on equal footing. |
| **Telematics** | Technology (usually a smartphone app or small plug-in device) that tracks how someone drives — speed, hard braking, phone use — and sends that data somewhere for scoring or analysis. |
| **UBI (Usage-Based Insurance)** | Car insurance where your rate is based partly on how you actually drive (from telematics data), not just your age, location, and history. Progressive Snapshot and State Farm Drive Safe & Save are well-known examples. |
| **Enrollment rate** | The percent of people who were offered the program and actually signed up. |
| **Retention** | The percent of people who signed up and are still actively participating later (this project tracks retention at the 12-month mark). |
| **KPI (Key Performance Indicator)** | A specific, measurable target used to judge whether the program is working — this project's two headline KPIs are a 5% reduction in speeding-related crashes and a 5% reduction in estimated emissions. |
| **ROI (Return on Investment)** | Whether the money put into the program comes back as savings, and how much: `(benefit − cost) ÷ cost`. A negative ROI means the program costs more than it currently saves. |
| **Loss ratio** | An insurance industry number: how much an insurer pays out in claims compared to how much it collects in premiums. A lower loss ratio is better for the insurer — it means claims cost less than what came in. |
| **Adverse selection** | The tendency for the people most likely to sign up for something like a discount program to already be the "better" customers (here, safer drivers), which can make a program look more effective than the average driver's behavior actually changed. |
| **Social cost of carbon** | A dollar estimate (here, $51 per metric ton of CO2) used by economists and government agencies to put a price on the damage caused by carbon emissions, so an emissions reduction can be compared against a dollar figure. |
| **Payback period** | How long it takes for a program's cumulative savings to catch up to and exceed its cumulative cost. This project's model shows that doesn't happen within the 3 years it projects, at its conservative assumptions. |
| **Composite / blended metric** | A single score built by combining more than one underlying number (here, the speeding-crash rate and fatal-crash rate) so counties can be ranked on one scale instead of several separate ones. |
