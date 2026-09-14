"""
Builds non-technical, presentation-layer visuals for RoadRisk: an executive
at-a-glance summary, a plain-language program flow diagram, and a cost vs.
benefit chart pulled from the financial model.

These are separate from county_risk_analysis.py, which produces the analytical
figures (risk ranking bar chart, rate-vs-population scatter). This script is
about explaining the *project* to a reader who won't open the spreadsheet.

Usage: python3 build_visuals.py
Outputs to analysis/figures/:
  - roadrisk_at_a_glance.png
  - how_the_program_works.png
  - cost_vs_benefit_by_year.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES = os.path.join(BASE, "analysis", "figures")
os.makedirs(FIGURES, exist_ok=True)

NAVY = "#1F4E78"
BLUE = "#2E75B6"
RED = "#C0392B"
GREEN = "#2E7D32"
GRAY = "#595959"
LIGHT = "#F2F2F2"


# ------------------------------------------------------------- Figure 1 ----
def build_at_a_glance():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    ax.text(5, 5.6, "RoadRisk: Pilot at a Glance", fontsize=22, fontweight="bold",
             ha="center", color=NAVY)
    ax.text(5, 5.15,
            "A state DOT + insurer telematics program targeting Pennsylvania's highest speeding-crash-risk counties",
            fontsize=11, ha="center", color=GRAY)

    stats = [
        ("67", "PA counties analyzed", "using real 2018-2020 PennDOT crash data"),
        ("10", "counties in the Year-1 pilot", "chosen for high risk + enough population to matter"),
        ("~5,900", "speeding-related crashes/yr", "in the pilot counties today, before the program"),
        ("2.18M", "residents in the pilot region", "the population the program aims to make safer"),
        ("5%", "Year-1 target reduction", "in speeding violations and estimated emissions"),
        ("~23,500", "drivers modeled to enroll", "by the end of Year 1, in the financial model"),
    ]

    cols, rows = 3, 2
    box_w, box_h = 2.9, 1.9
    gap_x, gap_y = 0.2, 0.25
    start_x, start_y = 0.15, 4.4
    for i, (num, label, sub) in enumerate(stats):
        r, c = divmod(i, cols)
        x = start_x + c * (box_w + gap_x)
        y = start_y - r * (box_h + gap_y)
        ax.add_patch(FancyBboxPatch((x, y - box_h), box_w, box_h,
                                     boxstyle="round,pad=0.02,rounding_size=0.08",
                                     linewidth=0, facecolor=LIGHT))
        ax.text(x + box_w / 2, y - 0.55, num, fontsize=26, fontweight="bold",
                 ha="center", color=BLUE)
        ax.text(x + box_w / 2, y - 1.05, label, fontsize=10.5, fontweight="bold",
                 ha="center", color=NAVY, wrap=True)
        ax.text(x + box_w / 2, y - 1.55, sub, fontsize=8.5, ha="center", color=GRAY,
                 wrap=True)

    ax.text(5, 0.15,
            "Source: PennDOT crash data (data.pa.gov) + 2020 Census, this repo's analysis/ and financial_model/",
            fontsize=8, ha="center", color=GRAY, style="italic")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "roadrisk_at_a_glance.png"), dpi=150, facecolor="white")
    plt.close(fig)
    print("Wrote roadrisk_at_a_glance.png")


# ------------------------------------------------------------- Figure 2 ----
def build_program_flow():
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.text(5.5, 3.9, "How the Program Works", fontsize=18, fontweight="bold",
             ha="center", color=NAVY)

    boxes = [
        (0.4, "State DOT", "Picks the highest-risk\ncounties using crash data\nand funds enrollment\nincentives", NAVY),
        (3.15, "Insurer Partner", "Offers a premium discount\nto drivers who opt into\ntelematics (phone-based\nspeed & braking tracking)", BLUE),
        (5.9, "Enrolled Driver", "Sees a weekly driving\nscore and real-time alerts,\nadjusts driving to earn\nthe discount", GREEN),
        (8.65, "Outcome", "Fewer speeding crashes,\nlower premiums,\nmeasurably cleaner\ndriving", RED),
    ]
    box_w, box_h, y0 = 2.15, 2.3, 0.9
    for x, title, body, color in boxes:
        ax.add_patch(FancyBboxPatch((x, y0), box_w, box_h,
                                     boxstyle="round,pad=0.02,rounding_size=0.1",
                                     linewidth=1.5, edgecolor=color, facecolor="white"))
        ax.text(x + box_w / 2, y0 + box_h - 0.35, title, fontsize=12, fontweight="bold",
                 ha="center", color=color)
        ax.text(x + box_w / 2, y0 + box_h / 2 - 0.25, body, fontsize=8.7, ha="center",
                 va="center", color=GRAY, linespacing=1.5)

    for x, _, _, _ in boxes[:-1]:
        arrow = FancyArrowPatch((x + box_w + 0.03, y0 + box_h / 2),
                                 (x + box_w + 0.55, y0 + box_h / 2),
                                 arrowstyle="-|>", mutation_scale=22, color=GRAY, linewidth=2)
        ax.add_patch(arrow)

    ax.text(5.5, 0.35,
            "Funded jointly: the state pays enrollment incentives + a share of admin; "
            "the insurer pays the discount + telematics licensing. See strategy/government_insurer_strategy.md",
            fontsize=8.5, ha="center", color=GRAY, style="italic")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "how_the_program_works.png"), dpi=150, facecolor="white")
    plt.close(fig)
    print("Wrote how_the_program_works.png")


# ------------------------------------------------------------- Figure 3 ----
def build_cost_vs_benefit():
    # Figures pulled from financial_model/RoadRisk_Financial_Model.xlsx (see that
    # workbook for the underlying formulas and assumptions).
    years = ["Year 1", "Year 2", "Year 3"]
    combined_cost = [6_385_587, 10_309_311, 13_821_867]
    combined_benefit = [3_165_949, 5_276_582, 7_387_215]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = range(len(years))
    w = 0.32
    b1 = ax.bar([i - w / 2 for i in x], combined_cost, width=w, label="Combined program cost",
                color=RED, alpha=0.85)
    b2 = ax.bar([i + w / 2 for i in x], combined_benefit, width=w, label="Combined benefit\n(state + insurer + emissions)",
                color=GREEN, alpha=0.85)

    for bars in (b1, b2):
        for rect in bars:
            h = rect.get_height()
            ax.annotate(f"${h/1e6:.1f}M", (rect.get_x() + rect.get_width() / 2, h),
                        textcoords="offset points", xytext=(0, 4), ha="center", fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(years, fontsize=11)
    ax.set_ylabel("$ (millions), nominal")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v/1e6:.0f}M")
    ax.set_title("Modeled Cost vs. Benefit, Combined (State + Insurer)", fontsize=14,
                 fontweight="bold", color=NAVY, pad=14)
    ax.legend(loc="upper left", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.5, -0.16,
            "At base-case assumptions the program does not fully pay back within 3 years -- see\n"
            "financial_model/RoadRisk_Financial_Model.xlsx (ROI Summary tab) for why, and what would close the gap.",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=GRAY, style="italic")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "cost_vs_benefit_by_year.png"), dpi=150, facecolor="white")
    plt.close(fig)
    print("Wrote cost_vs_benefit_by_year.png")


if __name__ == "__main__":
    build_at_a_glance()
    build_program_flow()
    build_cost_vs_benefit()
