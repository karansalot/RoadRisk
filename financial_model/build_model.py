"""
Builds RoadRisk_Financial_Model.xlsx: a 3-year financial + KPI tracking model
for the state DOT / insurer telematics safe-driving pilot described in
strategy/government_insurer_strategy.md, targeting the "scale tier" counties
identified in data/processed/pilot_shortlist_scale_tier.csv.

Run: python3 build_model.py
Then recalc with the xlsx skill's scripts/recalc.py before shipping.
"""

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT_NAME = "Arial"

BLUE = Font(name=FONT_NAME, color="0000FF")
BLACK = Font(name=FONT_NAME, color="000000")
GREEN = Font(name=FONT_NAME, color="008000")
BOLD = Font(name=FONT_NAME, bold=True)
BOLD_BLUE = Font(name=FONT_NAME, bold=True, color="0000FF")
BOLD_WHITE = Font(name=FONT_NAME, bold=True, color="FFFFFF")
TITLE = Font(name=FONT_NAME, bold=True, size=14)
SECTION = Font(name=FONT_NAME, bold=True, size=11, color="FFFFFF")
ITALIC_GRAY = Font(name=FONT_NAME, italic=True, color="595959", size=9)

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
SECTION_FILL = PatternFill("solid", fgColor="2E75B6")
INPUT_FILL = PatternFill("solid", fgColor="FFFFCC")
SUBTLE_FILL = PatternFill("solid", fgColor="F2F2F2")

THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

CUR0 = '$#,##0;($#,##0);"-"'
PCT0 = '0%;(0%);"-"'
PCT1 = '0.0%;(0.0%);"-"'
PCT2 = '0.00%;(0.00%);"-"'
NUM0 = '#,##0;(#,##0);"-"'


def style_header_row(ws, row, first_col, last_col, fill=HEADER_FILL, font=BOLD_WHITE):
    for c in range(first_col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = font
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BOX


def set_col_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def section_title(ws, row, text, last_col=5):
    ws.cell(row=row, column=1, value=text)
    for c in range(1, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = SECTION_FILL
        cell.font = SECTION
    ws.row_dimensions[row].height = 20


def note(ws, cell_ref, text):
    ws[cell_ref].comment = Comment(text, "RoadRisk model")


wb = openpyxl.Workbook()

# ============================================================== Read Me ====
ws = wb.active
ws.title = "Read Me"
set_col_widths(ws, [110])
ws["A1"] = "RoadRisk: Government-Insurer Telematics Program — Financial & KPI Tracking Model"
ws["A1"].font = TITLE
ws.row_dimensions[1].height = 20
ws["A3"] = (
    "Estimates and tracks the 3-year financial case for the pilot described in "
    "strategy/government_insurer_strategy.md, and gives the joint state/insurer steering "
    "committee a place to log real Year-1 KPI results against target."
)
ws["A3"].alignment = Alignment(wrap_text=True)
ws.row_dimensions[3].height = 30

tabs = [
    ("Assumptions", "Every input the model runs on. Edit the blue cells here — everything else recalculates. Each input cell has a comment naming its source."),
    ("Enrollment & Reach", "Converts the population assumption into an enrolled-driver count across 3 years."),
    ("Program Costs", "State and insurer cost by year — incentives, admin share, and telematics platform licensing."),
    ("Benefits & Savings", "Modeled avoided crashes, avoided cost, insurer claims benefit, and a monetized emissions estimate."),
    ("ROI Summary", "Net benefit, ROI %, and payback period, split State / Insurer / Combined."),
    ("KPI Dashboard", "Quarterly Year-1 enrollment tracker plus annual outcome KPIs. Fill in the yellow Actual cells as real data arrives."),
    ("Sensitivity", "What enrollment, per-enrollee effect, or insurer market share is needed to hit the 5% KPI — the base case alone does not reach it (see note on that tab)."),
]
r = 6
ws.cell(row=r, column=1, value="Tabs in this workbook").font = BOLD
r += 1
for name, desc in tabs:
    ws.cell(row=r, column=1, value=f"{name} — {desc}").alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 28
    r += 1

r += 1
ws.cell(row=r, column=1, value="Color legend").font = BOLD
r += 1
for txt, font, fill in [
    ("Blue text = hardcoded input / assumption you can change", BLUE, None),
    ("Black text = formula calculated within the same sheet", BLACK, None),
    ("Green text = formula that pulls a value from another sheet", GREEN, None),
    ("Yellow fill = fill in as the program runs (actuals)", BLACK, INPUT_FILL),
]:
    c = ws.cell(row=r, column=1, value=txt)
    c.font = font
    if fill:
        c.fill = fill
    r += 1

r += 1
ws.cell(row=r, column=1, value=(
    "All dollar figures are nominal USD, undiscounted, modeled at the program level (not a "
    "single household's premium). Every assumption cell carries a comment stating its source "
    "or that it is a program-design estimate. Underlying crash-data provenance is in "
    "data/SOURCES.md at the repo root."
)).alignment = Alignment(wrap_text=True)
ws.row_dimensions[r].height = 45

# ============================================================ Assumptions ==
ws = wb.create_sheet("Assumptions")
set_col_widths(ws, [52, 16, 12, 46])
ws["A1"] = "Assumptions"
ws["A1"].font = TITLE
style_header_row(ws, 2, 1, 4)
for c, t in zip("ABCD", ["Assumption", "Value", "Unit", "Note"]):
    ws[f"{c}2"] = t

row = 3
section_title(ws, row, "Population & Enrollment Universe", 4); row += 1

def add_input(ws, row, label_text, value, unit, comment_text, number_format=None):
    ws.cell(row=row, column=1, value=label_text)
    vcell = ws.cell(row=row, column=2, value=value)
    vcell.font = BLUE
    if number_format:
        vcell.number_format = number_format
    ws.cell(row=row, column=3, value=unit).font = ITALIC_GRAY
    note(ws, f"B{row}", comment_text)
    return row

R_POP = add_input(ws, row, "Scale-tier pilot population (2020 Census)", 2175496, "residents",
    "Sum of 2020 Census population across the 10 scale-tier counties in "
    "data/processed/pilot_shortlist_scale_tier.csv (Monroe, Fayette, Dauphin, York, Mercer, "
    "Lebanon, Franklin, Lackawanna, Lehigh, Lycoming).", NUM0)
row += 1
R_LICENSED_PCT = add_input(ws, row, "Licensed drivers as % of population", 0.75, "%",
    "Program-design estimate consistent with published FHWA Highway Statistics ratios of "
    "licensed drivers to total population (typically 72-78% nationally).", PCT1)
row += 1
R_MKT_SHARE = add_input(ws, row, "Insurer partner's market share of licensed drivers in pilot counties", 0.12, "%",
    "Assumption: a single mid-size regional carrier partner. Modeled explicitly because it is "
    "the main lever limiting how much a single-carrier pilot can move a county-wide KPI — see "
    "the Sensitivity tab.", PCT1)
row += 1
ws.cell(row=row, column=1, value="Eligible policyholder base (computed)")
ws.cell(row=row, column=2, value=f"=B{R_POP}*B{R_LICENSED_PCT}*B{R_MKT_SHARE}").font = BLACK
ws.cell(row=row, column=2).number_format = NUM0
ws.cell(row=row, column=3, value="policyholders").font = ITALIC_GRAY
R_ELIGIBLE = row
row += 2

section_title(ws, row, "Enrollment Ramp & Retention", 4); row += 1
R_ENR_Y1 = add_input(ws, row, "Year 1 enrollment (% of eligible policyholders)", 0.12, "%",
    "Matches the Year-1 enrollment KPI target in government_insurer_strategy.md.", PCT1); row += 1
R_ENR_Y2 = add_input(ws, row, "Year 2 enrollment (% of eligible policyholders)", 0.20, "%",
    "Program-design ramp assumption for the Year-2 expansion phase.", PCT1); row += 1
R_ENR_Y3 = add_input(ws, row, "Year 3 enrollment (% of eligible policyholders)", 0.28, "%",
    "Program-design ramp assumption.", PCT1); row += 1
R_RETENTION = add_input(ws, row, "Retention: enrollees still active at month 12", 0.70, "%",
    "Matches the Year-1 retention KPI target in government_insurer_strategy.md.", PCT1); row += 2

section_title(ws, row, "Cost Assumptions", 4); row += 1
R_INCENTIVE = add_input(ws, row, "State one-time enrollment incentive (per new enrollee)", 25, "$",
    "Program-design estimate (e.g., a DMV renewal fee credit or gift card), sized to the range "
    "shown to meaningfully lift opt-in in the market research brief.", CUR0); row += 1
R_ADMIN_TOTAL = add_input(ws, row, "Total program admin & marketing cost per year", 500000, "$/yr",
    "Program-design estimate: joint steering committee staff time, co-branded marketing "
    "through DOT/DMV channels, and third-party evaluation.", CUR0); row += 1
R_ADMIN_STATE_SHARE = add_input(ws, row, "State share of admin & marketing cost", 0.40, "%",
    "Program-design assumption; revisit annually per the strategy doc's governance section.", PCT1); row += 1
ws.cell(row=row, column=1, value="Insurer share of admin & marketing cost (computed)")
ws.cell(row=row, column=2, value=f"=1-B{R_ADMIN_STATE_SHARE}").font = BLACK
ws.cell(row=row, column=2).number_format = PCT1
R_ADMIN_INSURER_SHARE = row
row += 1
R_TELEMATICS_COST = add_input(ws, row, "Telematics platform licensing cost, per enrolled driver/year", 8, "$/driver/yr",
    "Program-design estimate for smartphone-based telematics SaaS at pilot scale; a dongle "
    "fallback in low-connectivity counties would add hardware cost not modeled here.", CUR0); row += 1
R_DISCOUNT_PCT = add_input(ws, row, "Insurer clean-driving premium discount", 0.15, "%",
    "Midpoint of the 10-20% target discount range in government_insurer_strategy.md.", PCT1); row += 1
R_AVG_PREMIUM = add_input(ws, row, "Average annual auto premium per policy, pilot region", 1450, "$/policy/yr",
    "Program-design estimate in line with published average PA auto premium levels; replace "
    "with the insurer partner's actual book average once selected.", CUR0); row += 2

section_title(ws, row, "Safety Effect & Avoided-Cost Assumptions", 4); row += 1
R_BASE_RATE = add_input(ws, row, "Baseline speeding-related crashes/year, scale-tier counties", 5892, "crashes/yr",
    "From data/processed/county_risk_scores.csv (avg annual speeding-related crashes, "
    "2018-2020, summed across the 10 scale-tier counties): 5,892.", NUM0); row += 1
R_EFFECT = add_input(ws, row, "Per-enrollee reduction in speeding-related crash involvement", 0.20, "%",
    "Conservative vs. published single-carrier UBI studies reporting 10-30% reductions in "
    "hard-braking/speeding events among enrollees; used here for the whole-crash-involvement "
    "effect, which is a stricter bar than an event-rate reduction.", PCT1); row += 1
R_STATE_COST_PER_CRASH = add_input(ws, row, "State cost avoided per prevented crash (emergency response + infrastructure)", 9500, "$/crash",
    "Program-design estimate: the state-borne subset of a comprehensive crash cost (excludes "
    "medical and lost-productivity costs, which fall on other parties), informed by the "
    "methodology in NHTSA's 'Economic and Societal Impact of Motor Vehicle Crashes.'", CUR0); row += 1
R_INSURER_CLAIM_COST = add_input(ws, row, "Insurer average claim cost per speeding-related crash", 12000, "$/crash",
    "Program-design estimate for a blended physical-damage + bodily-injury claim severity on "
    "a speeding-related loss; replace with the insurer partner's actual book severity.", CUR0); row += 1
R_LOSS_RATIO = add_input(ws, row, "Average loss ratio, enrolled book (claims cost / earned premium)", 0.65, "%",
    "Typical U.S. private-passenger auto industry loss ratio range (~60-70%); the discount is "
    "underwritten against the whole book's loss ratio, not just speeding-related claims, which "
    "is why this is modeled separately from the per-crash avoided cost above.", PCT1); row += 1
R_LOSS_RATIO_IMPROVEMENT = add_input(ws, row, "Loss-ratio improvement for enrolled cohort (behavior change + adverse selection)", 0.12, "%",
    "Program-design estimate toward the higher end of published telematics/UBI studies, which "
    "report mid-single-digit to ~15% relative loss-cost improvement for engaged/enrolled "
    "cohorts (safer drivers self-select to enroll, on top of any behavior change). Even at this "
    "favorable end of the range, the ROI Summary tab shows the insurer's discount cost is not "
    "fully offset within 3 years -- see the note there.", PCT1); row += 2

section_title(ws, row, "Emissions Assumptions", 4); row += 1
R_CO2_PER_DRIVER = add_input(ws, row, "Modeled CO2 reduction per enrolled driver per year", 0.12, "metric tons",
    "Modeled, not directly metered: derived from the EPA MOVES relationship between reduced "
    "speed variance / harsh acceleration and fuel consumption. Treat as an estimate pending "
    "telematics-vendor validation once the pilot is live — see the KPI note on this tab and "
    "in government_insurer_strategy.md.", '0.00'); row += 1
R_SCC = add_input(ws, row, "Social cost of carbon (for illustrative monetization only)", 51, "$/metric ton",
    "2021 Interagency Working Group central estimate (2020$, 3% discount rate). Used only to "
    "size the emissions benefit for the public-value ROI view — not part of the state or "
    "insurer P&L.", CUR0); row += 2

section_title(ws, row, "KPI Targets (Year 1)", 4); row += 1
R_KPI_SPEED = add_input(ws, row, "Speeding-related crash reduction target (population level)", 0.05, "%",
    "Year-1 KPI target from government_insurer_strategy.md.", PCT1); row += 1
R_KPI_EMISSIONS = add_input(ws, row, "Emissions reduction target (modeled, enrolled drivers)", 0.05, "%",
    "Year-1 KPI target from government_insurer_strategy.md.", PCT1); row += 1

A = "Assumptions"


def aref(row, col="B"):
    return f"'{A}'!${col}${row}"


# ==================================================== Enrollment & Reach ===
ws = wb.create_sheet("Enrollment & Reach")
set_col_widths(ws, [42, 16, 16, 16, 40])
ws["A1"] = "Enrollment & Reach"
ws["A1"].font = TITLE
style_header_row(ws, 3, 1, 4)
for c, t in zip("ABCD", ["", "Year 1", "Year 2", "Year 3"]):
    ws[f"{c}3"] = t

ws["A4"] = "Eligible policyholder base"
for col in "BCD":
    cell = ws[f"{col}4"]
    cell.value = f"={aref(R_ELIGIBLE)}"
    cell.font = GREEN
    cell.number_format = NUM0

ws["A5"] = "Enrollment rate (% of eligible)"
for col, r in zip("BCD", [R_ENR_Y1, R_ENR_Y2, R_ENR_Y3]):
    cell = ws[f"{col}5"]
    cell.value = f"={aref(r)}"
    cell.font = GREEN
    cell.number_format = PCT1

ws["A6"] = "Enrolled drivers (that year, cumulative)"
for col in "BCD":
    cell = ws[f"{col}6"]
    cell.value = f"={col}4*{col}5"
    cell.font = BLACK
    cell.number_format = NUM0
ROW_ENROLLED = 6

ws["A7"] = "Retained from prior year's cohort (active at month 12)"
ws["B7"] = 0
ws["B7"].font = BLACK
ws["B7"].number_format = NUM0
ws["C7"] = f"=B{ROW_ENROLLED}*{aref(R_RETENTION)}"
ws["C7"].font = BLACK
ws["C7"].number_format = NUM0
ws["D7"] = f"=C{ROW_ENROLLED}*{aref(R_RETENTION)}"
ws["D7"].font = BLACK
ws["D7"].number_format = NUM0
ROW_RETAINED = 7

ws["A8"] = "New enrollees this year (drives the one-time incentive cost)"
ws["B8"] = f"=B{ROW_ENROLLED}"
ws["B8"].font = BLACK
ws["B8"].number_format = NUM0
for col in "CD":
    prev = "B" if col == "C" else "C"
    cell = ws[f"{col}8"]
    cell.value = f"=MAX(0,{col}{ROW_ENROLLED}-{prev}{ROW_RETAINED})"
    cell.font = BLACK
    cell.number_format = NUM0
ROW_NEW = 8

ws["A9"] = "Share of pilot-county licensed drivers reached (enrolled / total drivers)"
for col in "BCD":
    cell = ws[f"{col}9"]
    cell.value = f"={col}{ROW_ENROLLED}/({aref(R_POP)}*{aref(R_LICENSED_PCT)})"
    cell.font = BLACK
    cell.number_format = PCT2
ROW_SHARE = 9

ws.row_dimensions[11].height = 5
ws["A12"] = (
    "Enrolled drivers are modeled as that year's active cohort size, not a running total across "
    "years, to keep the cost/benefit math tied to who is actually active in a given year."
)
ws["A12"].font = ITALIC_GRAY
ws["A12"].alignment = Alignment(wrap_text=True)

ENROLL_SHEET = "Enrollment & Reach"


def eref(row, col):
    return f"'{ENROLL_SHEET}'!${col}${row}"


# ========================================================= Program Costs ==
ws = wb.create_sheet("Program Costs")
set_col_widths(ws, [42, 16, 16, 16, 40])
ws["A1"] = "Program Costs"
ws["A1"].font = TITLE
style_header_row(ws, 3, 1, 4)
for c, t in zip("ABCD", ["", "Year 1", "Year 2", "Year 3"]):
    ws[f"{c}3"] = t

row = 4
section_title(ws, row, "State Costs", 4); row += 1
ws.cell(row=row, column=1, value="One-time enrollment incentive")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={eref(ROW_NEW, col)}*{aref(R_INCENTIVE)}")
    cell.font = GREEN
    cell.number_format = CUR0
ROW_STATE_INCENTIVE = row
row += 1
ws.cell(row=row, column=1, value="State share of admin & marketing cost")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={aref(R_ADMIN_TOTAL)}*{aref(R_ADMIN_STATE_SHARE)}")
    cell.font = GREEN
    cell.number_format = CUR0
ROW_STATE_ADMIN = row
row += 1
ws.cell(row=row, column=1, value="Total state cost").font = BOLD
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={col}{ROW_STATE_INCENTIVE}+{col}{ROW_STATE_ADMIN}")
    cell.font = BOLD
    cell.number_format = CUR0
ROW_STATE_TOTAL = row
row += 2

section_title(ws, row, "Insurer Costs", 4); row += 1
ws.cell(row=row, column=1, value="Premium discount paid to enrollees")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={eref(ROW_ENROLLED, col)}*{aref(R_AVG_PREMIUM)}*{aref(R_DISCOUNT_PCT)}")
    cell.font = GREEN
    cell.number_format = CUR0
ROW_INS_DISCOUNT = row
row += 1
ws.cell(row=row, column=1, value="Telematics platform licensing")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={eref(ROW_ENROLLED, col)}*{aref(R_TELEMATICS_COST)}")
    cell.font = GREEN
    cell.number_format = CUR0
ROW_INS_TELEMATICS = row
row += 1
ws.cell(row=row, column=1, value="Insurer share of admin & marketing cost")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={aref(R_ADMIN_TOTAL)}*{aref(R_ADMIN_INSURER_SHARE)}")
    cell.font = GREEN
    cell.number_format = CUR0
ROW_INS_ADMIN = row
row += 1
ws.cell(row=row, column=1, value="Total insurer cost").font = BOLD
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_INS_DISCOUNT}+{col}{ROW_INS_TELEMATICS}+{col}{ROW_INS_ADMIN}")
    cell.font = BOLD
    cell.number_format = CUR0
ROW_INS_TOTAL = row
row += 2

ws.cell(row=row, column=1, value="Combined program cost").font = BOLD
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={col}{ROW_STATE_TOTAL}+{col}{ROW_INS_TOTAL}")
    cell.font = BOLD
    cell.number_format = CUR0
    cell.fill = SUBTLE_FILL
ROW_COMBINED_COST = row

COST_SHEET = "Program Costs"


def cref(row, col):
    return f"'{COST_SHEET}'!${col}${row}"


# ======================================================= Benefits & Savings
ws = wb.create_sheet("Benefits & Savings")
set_col_widths(ws, [46, 16, 16, 16, 44])
ws["A1"] = "Benefits & Savings"
ws["A1"].font = TITLE
style_header_row(ws, 3, 1, 4)
for c, t in zip("ABCD", ["", "Year 1", "Year 2", "Year 3"]):
    ws[f"{c}3"] = t

row = 4
section_title(ws, row, "Crash Reduction (drives both state and insurer benefit)", 4); row += 1
ws.cell(row=row, column=1, value="Baseline speeding-related crashes/year, scale-tier counties")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={aref(R_BASE_RATE)}")
    cell.font = GREEN
    cell.number_format = NUM0
ROW_BASELINE = row
row += 1
ws.cell(row=row, column=1, value="Prevented crashes (enrolled drivers' share x per-enrollee effect)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_BASELINE}*{eref(ROW_SHARE, col)}*{aref(R_EFFECT)}")
    cell.font = BLACK
    cell.number_format = NUM0
ROW_PREVENTED = row
row += 1
ws.cell(row=row, column=1, value="Population-level speeding-crash reduction (modeled, vs. 5% KPI)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={col}{ROW_PREVENTED}/{col}{ROW_BASELINE}")
    cell.font = BLACK
    cell.number_format = PCT2
ROW_POP_REDUCTION = row
row += 2

section_title(ws, row, "State Benefit", 4); row += 1
ws.cell(row=row, column=1, value="Avoided emergency-response & infrastructure cost")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_PREVENTED}*{aref(R_STATE_COST_PER_CRASH)}")
    cell.font = BLACK
    cell.number_format = CUR0
ROW_STATE_BENEFIT = row
row += 2

section_title(ws, row, "Insurer Benefit", 4); row += 1
ws.cell(row=row, column=1, value="Avoided claims cost (speeding-related crashes prevented)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_PREVENTED}*{aref(R_INSURER_CLAIM_COST)}")
    cell.font = BLACK
    cell.number_format = CUR0
ROW_INSURER_BENEFIT_NARROW = row
row += 1
ws.cell(row=row, column=1, value="Avoided claims cost (broader enrolled-book loss-ratio improvement)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=(f"={eref(ROW_ENROLLED, col)}*{aref(R_AVG_PREMIUM)}"
                           f"*{aref(R_LOSS_RATIO)}*{aref(R_LOSS_RATIO_IMPROVEMENT)}"))
    cell.font = GREEN
    cell.number_format = CUR0
ROW_INSURER_BENEFIT_BROAD = row
row += 1
ws.cell(row=row, column=1, value="Total insurer benefit").font = BOLD
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_INSURER_BENEFIT_NARROW}+{col}{ROW_INSURER_BENEFIT_BROAD}")
    cell.font = BOLD
    cell.number_format = CUR0
ROW_INSURER_BENEFIT = row
row += 2

section_title(ws, row, "Emissions (public-value estimate, not on either party's P&L)", 4); row += 1
ws.cell(row=row, column=1, value="Modeled CO2 reduction (metric tons)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={eref(ROW_ENROLLED, col)}*{aref(R_CO2_PER_DRIVER)}")
    cell.font = BLACK
    cell.number_format = NUM0
ROW_CO2 = row
row += 1
ws.cell(row=row, column=1, value="Emissions reduction vs. 5% KPI target")
ws.cell(row=row, column=1).font = BLACK
note(ws, f"A{row}",
     "The 5% emissions KPI is a modeled, per-enrolled-driver reduction vs. each driver's own "
     "pre-enrollment baseline (see government_insurer_strategy.md) -- it is tracked directly on "
     "the KPI Dashboard tab from telematics data, not derived from this tab's population-wide "
     "CO2 tonnage, which instead sizes the public-value dollar estimate below.")
row += 1
ws.cell(row=row, column=1, value="Monetized emissions value (social cost of carbon)")
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={col}{ROW_CO2}*{aref(R_SCC)}")
    cell.font = BLACK
    cell.number_format = CUR0
ROW_EMISSIONS_VALUE = row
row += 2

ws.cell(row=row, column=1, value="Combined benefit (state + insurer + emissions public value)").font = BOLD
for col in "BCD":
    cell = ws.cell(row=row, column="BCD".index(col) + 2,
                    value=f"={col}{ROW_STATE_BENEFIT}+{col}{ROW_INSURER_BENEFIT}+{col}{ROW_EMISSIONS_VALUE}")
    cell.font = BOLD
    cell.number_format = CUR0
    cell.fill = SUBTLE_FILL
ROW_COMBINED_BENEFIT = row
row += 2

ws.cell(row=row, column=1, value=(
    "Note: at the 20% per-enrollee effect and 12% single-carrier market-share assumptions on the "
    "Assumptions tab, the modeled population-level reduction above is well under the 5% KPI "
    "target -- see the Sensitivity tab for what it would take to close that gap."
)).alignment = Alignment(wrap_text=True)
ws.cell(row=row, column=1).font = ITALIC_GRAY
ws.row_dimensions[row].height = 45

BENEFIT_SHEET = "Benefits & Savings"


def bref(row, col):
    return f"'{BENEFIT_SHEET}'!${col}${row}"


# ============================================================= ROI Summary
ws = wb.create_sheet("ROI Summary")
set_col_widths(ws, [38, 16, 16, 16, 16, 40])
ws["A1"] = "ROI Summary"
ws["A1"].font = TITLE
style_header_row(ws, 3, 1, 5)
for c, t in zip("ABCDE", ["", "Year 1", "Year 2", "Year 3", "3-Year Total"]):
    ws[f"{c}3"] = t


def block(ws, row, title, cost_row_ref_fn, benefit_row_ref_fn):
    section_title(ws, row, title, 5); row += 1
    ws.cell(row=row, column=1, value="Cost")
    for col in "BCD":
        cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={cost_row_ref_fn(col)}")
        cell.font = GREEN
        cell.number_format = CUR0
    ws.cell(row=row, column=5, value=f"=SUM(B{row}:D{row})").number_format = CUR0
    ws.cell(row=row, column=5).font = BOLD
    row_cost = row
    row += 1
    ws.cell(row=row, column=1, value="Benefit")
    for col in "BCD":
        cell = ws.cell(row=row, column="BCD".index(col) + 2, value=f"={benefit_row_ref_fn(col)}")
        cell.font = GREEN
        cell.number_format = CUR0
    ws.cell(row=row, column=5, value=f"=SUM(B{row}:D{row})").number_format = CUR0
    ws.cell(row=row, column=5).font = BOLD
    row_benefit = row
    row += 1
    ws.cell(row=row, column=1, value="Net benefit").font = BOLD
    for col in "BCDE":
        cell = ws.cell(row=row, column="BCDE".index(col) + 2, value=f"={col}{row_benefit}-{col}{row_cost}")
        cell.font = BOLD
        cell.number_format = CUR0
    row_net = row
    row += 1
    ws.cell(row=row, column=1, value="ROI % (net benefit / cost)")
    for col in "BCDE":
        cell = ws.cell(row=row, column="BCDE".index(col) + 2, value=f"=IFERROR({col}{row_net}/{col}{row_cost},0)")
        cell.number_format = PCT1
    row_roi = row
    row += 2
    return row, row_cost, row_benefit, row_net, row_roi


row = 4
row, SC, SB, SN, SR = block(
    ws, row, "State",
    lambda col: cref(ROW_STATE_TOTAL, col),
    lambda col: bref(ROW_STATE_BENEFIT, col),
)
row, IC, IB, IN, IR = block(
    ws, row, "Insurer",
    lambda col: cref(ROW_INS_TOTAL, col),
    lambda col: bref(ROW_INSURER_BENEFIT, col),
)
row, CC, CB, CN, CR = block(
    ws, row, "Combined (incl. public-value emissions benefit)",
    lambda col: cref(ROW_COMBINED_COST, col),
    lambda col: bref(ROW_COMBINED_BENEFIT, col),
)

section_title(ws, row, "Payback", 5); row += 1
ws.cell(row=row, column=1, value="Cumulative combined net benefit")
ws.cell(row=row, column=2, value=f"=B{CN}").number_format = CUR0
ws.cell(row=row, column=3, value=f"=B{row}+C{CN}").number_format = CUR0
ws.cell(row=row, column=4, value=f"=C{row}+D{CN}").number_format = CUR0
for col in "BCD":
    ws.cell(row=row, column="BCD".index(col) + 2).font = BLACK
ROW_CUM_NET = row
row += 1
ws.cell(row=row, column=1, value="Payback status")
ws.cell(row=row, column=2, value=(
    f'=_xlfn.IFS(B{ROW_CUM_NET}>=0,"Positive in Year 1",'
    f'C{ROW_CUM_NET}>=0,"Positive in Year 2",'
    f'D{ROW_CUM_NET}>=0,"Positive in Year 3",'
    f'TRUE,"Not within 3 years")'
))
row += 2

ws.cell(row=row, column=1, value=(
    "Reading this honestly: at base-case assumptions, the program does not pay back within 3 "
    "years for the insurer or in combined terms, because the premium discount is paid on the "
    "insurer's full enrolled book while the claims-cost benefit only accrues where behavior "
    "actually changes or better risks self-select in -- a well-documented tension in real UBI "
    "economics, not a modeling error. Three things would close the gap, individually or "
    "combined: (1) a lower or score-tiered discount instead of a flat 15% to every enrollee, "
    "(2) retained cohorts compounding the loss-ratio benefit over a longer, multi-cohort "
    "horizon than this 3-year window captures, and (3) counting the public value the state "
    "captures outside its own P&L (avoided injuries and fatalities beyond the narrow emergency-"
    "response/infrastructure cost line) -- which is real value the state is funding for, even "
    "though it is not monetized in the Combined row above. See the Sensitivity tab for the "
    "separate question of what it takes to hit the 5% crash-reduction KPI itself."
)).alignment = Alignment(wrap_text=True)
ws.row_dimensions[row].height = 100

# ============================================================ KPI Dashboard
ws = wb.create_sheet("KPI Dashboard")
set_col_widths(ws, [26, 16, 16, 16, 16])
ws["A1"] = "KPI Dashboard — Year 1"
ws["A1"].font = TITLE
ws["A2"] = "Fill in the yellow Actual cells as real program data arrives."
ws["A2"].font = ITALIC_GRAY

row = 4
section_title(ws, row, "Enrollment Ramp (cumulative % of eligible policyholders)", 5); row += 1
style_header_row(ws, row, 1, 5)
for c, t in zip("ABCDE", ["Quarter", "Target", "Actual", "Variance", "Status"]):
    ws.cell(row=row, column="ABCDE".index(c) + 1, value=t)
row += 1
q_targets = [0.25, 0.50, 0.75, 1.00]  # fraction of the Year-1 target ramped in linearly
first_enroll_row = row
for i, q in enumerate(["Q1", "Q2", "Q3", "Q4"]):
    ws.cell(row=row, column=1, value=q)
    tcell = ws.cell(row=row, column=2, value=f"={aref(R_ENR_Y1)}*{q_targets[i]}")
    tcell.font = GREEN
    tcell.number_format = PCT1
    acell = ws.cell(row=row, column=3, value=None)
    acell.fill = INPUT_FILL
    acell.number_format = PCT1
    vcell = ws.cell(row=row, column=4, value=f'=IFERROR(C{row}-B{row},"")')
    vcell.number_format = PCT1
    scell = ws.cell(row=row, column=5, value=f'=IF(C{row}="","",IF(C{row}>=B{row},"On track","Below target"))')
    row += 1
last_enroll_row = row - 1
row += 1

section_title(ws, row, "Retention (% of enrollees active, measured at month 12)", 5); row += 1
style_header_row(ws, row, 1, 5)
for c, t in zip("ABCDE", ["", "Target", "Actual", "Variance", "Status"]):
    ws.cell(row=row, column="ABCDE".index(c) + 1, value=t)
row += 1
ws.cell(row=row, column=1, value="Year 1")
tcell = ws.cell(row=row, column=2, value=f"={aref(R_RETENTION)}")
tcell.font = GREEN
tcell.number_format = PCT1
acell = ws.cell(row=row, column=3, value=None)
acell.fill = INPUT_FILL
acell.number_format = PCT1
ws.cell(row=row, column=4, value=f'=IFERROR(C{row}-B{row},"")').number_format = PCT1
ws.cell(row=row, column=5, value=f'=IF(C{row}="","",IF(C{row}>=B{row},"On track","Below target"))')
row += 2

section_title(ws, row, "Annual Outcome KPIs (Year 1, population-level vs. prior year)", 5); row += 1
style_header_row(ws, row, 1, 5)
for c, t in zip("ABCDE", ["KPI", "Target", "Actual", "Variance", "Status"]):
    ws.cell(row=row, column="ABCDE".index(c) + 1, value=t)
row += 1
ws.cell(row=row, column=1, value="Speeding-related crash reduction")
tcell = ws.cell(row=row, column=2, value=f"={aref(R_KPI_SPEED)}")
tcell.font = GREEN
tcell.number_format = PCT1
acell = ws.cell(row=row, column=3, value=None)
acell.fill = INPUT_FILL
acell.number_format = PCT1
note(ws, f"C{row}",
     "Enter the actual year-over-year change in PennDOT-reported speeding-related crashes for "
     "the pilot counties vs. the matched control-county group (see government_insurer_"
     "strategy.md KPI table).")
ws.cell(row=row, column=4, value=f'=IFERROR(C{row}-B{row},"")').number_format = PCT1
ws.cell(row=row, column=5, value=f'=IF(C{row}="","",IF(C{row}>=B{row},"On track","Below target"))')
row += 1
ws.cell(row=row, column=1, value="Emissions reduction (modeled)")
tcell = ws.cell(row=row, column=2, value=f"={aref(R_KPI_EMISSIONS)}")
tcell.font = GREEN
tcell.number_format = PCT1
acell = ws.cell(row=row, column=3, value=None)
acell.fill = INPUT_FILL
acell.number_format = PCT1
note(ws, f"C{row}",
     "Enter the actual modeled reduction reported by the telematics vendor (average enrolled-"
     "driver speed-variance/harsh-event reduction converted to estimated fuel/CO2 savings) -- "
     "this KPI is inherently modeled, not directly metered; see the caveat in the Assumptions tab.")
ws.cell(row=row, column=4, value=f'=IFERROR(C{row}-B{row},"")').number_format = PCT1
ws.cell(row=row, column=5, value=f'=IF(C{row}="","",IF(C{row}>=B{row},"On track","Below target"))')
row += 2

ws.cell(row=row, column=1, value=(
    "Enrollment quarterly targets ramp linearly to the Year-1 enrollment assumption (25/50/75/"
    "100% of the annual target by quarter) as a planning baseline -- replace with the steering "
    "committee's actual enrollment-campaign schedule once set."
)).alignment = Alignment(wrap_text=True)
ws.row_dimensions[row].height = 40

# ============================================================= Sensitivity
ws = wb.create_sheet("Sensitivity")
set_col_widths(ws, [30, 13, 13, 13, 13, 13, 4, 60])
ws["A1"] = "Sensitivity — Closing the Gap to the 5% Population-Level KPI"
ws["A1"].font = TITLE
ws["A3"] = (
    "At this workbook's base-case assumptions (12% single-carrier market share, 20% per-"
    "enrollee effect, Year-1 enrollment per the Assumptions tab), the modeled population-level "
    "speeding-crash reduction is well under the 5% target -- see the Year-1 figure below the "
    "grid. This is an intentional, honest gap: a single insurer's book cannot move a county-wide "
    "KPI on its own at realistic enrollment and effect sizes. The grid shows what combination of "
    "enrollment and per-enrollee effect gets there, holding market share fixed at its current "
    "12% assumption; the note below it shows the alternative lever -- a larger, multi-carrier "
    "market share."
)
ws["A3"].alignment = Alignment(wrap_text=True)
ws.row_dimensions[3].height = 100

row = 6
ws.cell(row=row, column=1, value="Population-level reduction (%)").font = BOLD
ws.cell(row=row, column=1).fill = SUBTLE_FILL
enroll_scenarios = [0.10, 0.15, 0.20, 0.25, 0.30]
effect_scenarios = [0.15, 0.20, 0.25, 0.30, 0.35]
for j, eff in enumerate(effect_scenarios):
    c = ws.cell(row=row, column=2 + j, value=eff)
    c.font = BOLD
    c.number_format = PCT0
    c.fill = SUBTLE_FILL
ws.cell(row=row, column=1, value="Enrollment ↓ / Per-enrollee effect →").font = BOLD
row += 1
grid_top = row
for i, enr in enumerate(enroll_scenarios):
    rcell = ws.cell(row=row, column=1, value=enr)
    rcell.font = BOLD
    rcell.number_format = PCT0
    rcell.fill = SUBTLE_FILL
    for j, eff in enumerate(effect_scenarios):
        col = 2 + j
        cell = ws.cell(row=row, column=col,
                        value=f"=$A{row}*{aref(R_LICENSED_PCT)}*{aref(R_MKT_SHARE)}*{get_column_letter(col)}$6")
        cell.number_format = PCT1
        cell.font = BLACK
        if enr == 0.20 and eff == 0.25:
            cell.fill = PatternFill("solid", fgColor="FFE699")
    row += 1
grid_bottom = row - 1
row += 1

ws.cell(row=row, column=1, value="Base-case Year 1 (from Enrollment & Reach / Benefits & Savings tabs)")
ws.cell(row=row, column=1).font = BOLD
cell = ws.cell(row=row, column=2, value=f"={bref(ROW_POP_REDUCTION,'B')}")
cell.font = GREEN
cell.number_format = PCT2
ws.cell(row=row, column=3, value="vs. KPI target")
tcell = ws.cell(row=row, column=4, value=f"={aref(R_KPI_SPEED)}")
tcell.font = GREEN
tcell.number_format = PCT1
row += 2

section_title(ws, row, "Alternative lever: combined market share needed (multi-carrier consortium)", 6); row += 1
ws.cell(row=row, column=1, value="Assumed enrollment rate for this calc")
ecell = ws.cell(row=row, column=2, value=0.20)
ecell.font = BLUE
ecell.number_format = PCT0
ROW_SENS_ENROLL = row
row += 1
ws.cell(row=row, column=1, value="Assumed per-enrollee effect for this calc")
fcell = ws.cell(row=row, column=2, value=0.25)
fcell.font = BLUE
fcell.number_format = PCT0
ROW_SENS_EFFECT = row
row += 1
ws.cell(row=row, column=1, value="Combined market share required to hit the 5% KPI").font = BOLD
cell = ws.cell(row=row, column=2,
    value=f"=IFERROR({aref(R_KPI_SPEED)}/({aref(R_LICENSED_PCT)}*B{ROW_SENS_ENROLL}*B{ROW_SENS_EFFECT}),\"n/a\")")
cell.font = BOLD
cell.number_format = PCT0
row += 1
ws.cell(row=row, column=1, value=(
    "At 20% enrollment and a 25% per-enrollee effect, hitting the 5% KPI needs roughly this "
    "share of pilot-county licensed drivers under a participating insurer -- i.e., recruiting a "
    "second or third carrier into the pilot in Year 2, per the phasing in government_insurer_"
    "strategy.md, rather than assuming a single 12%-share carrier can do it alone."
)).alignment = Alignment(wrap_text=True)
ws.row_dimensions[row].height = 45

wb.save("RoadRisk_Financial_Model.xlsx")
print("Sensitivity sheet written. All sheets complete.")
