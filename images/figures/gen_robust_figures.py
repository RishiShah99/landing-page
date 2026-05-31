"""Figures for the Architecture-Driven Adversarial Robustness page.

Cream paper palette to match the rest of the portfolio. Generates:
  - robust_fig2_cross_attack.png : cross-attack gain bars (Baseline vs Ours)
                                   across FGSM, PGD, CW, Patch. Headline figure
                                   of §4. Numbers are from the page abstract.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PAPER = "#f3ece0"
CARD = "#f9f3e6"
INK = "#1d1a16"
GOLD = "#b18639"
SAGE_BG = "#d8e4d4"
SAGE_INK = "#2f4a36"
MUTED = "#8a7f6a"


def setup_rc():
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["EB Garamond", "Garamond", "DejaVu Serif"],
            "font.size": 12,
            "axes.titlesize": 13,
            "axes.labelsize": 12,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "figure.facecolor": CARD,
            "axes.facecolor": CARD,
            "savefig.facecolor": CARD,
            "savefig.edgecolor": "none",
        }
    )


def cross_attack(outpath: Path):
    """Gain-over-baseline bars across four attack families.

    Numbers from the §4 skeleton: FGSM +8 pp, PGD +12 pp, CW +9 pp, Patch +7 pp.
    Only the gain is plotted because the absolute baselines for FGSM / CW / Patch
    are not reported in the source material. This keeps the figure honest: it
    shows the consistency-of-gain story without fabricated absolute numbers.
    """
    attacks = ["FGSM", "PGD", "CW", "Patch"]
    gains_pp = np.array([8, 12, 9, 7], dtype=float)

    fig, ax = plt.subplots(figsize=(7.8, 3.6), dpi=200)
    y = np.arange(len(attacks))[::-1]

    bars = ax.barh(y, gains_pp, color=GOLD, height=0.55)

    for i, (yi, g) in enumerate(zip(y, gains_pp)):
        ax.text(
            g + 0.3,
            yi,
            f"+{int(g)} pp",
            ha="left",
            va="center",
            fontsize=12,
            color=SAGE_INK,
            fontweight="bold",
        )

    ax.set_yticks(y)
    ax.set_yticklabels(attacks)
    ax.set_xlabel("Gain over baseline CORnet-S (percentage points)")
    ax.set_xlim(0, 15)
    ax.set_xticks([0, 4, 8, 12])
    ax.set_xticklabels(["0", "+4", "+8", "+12"])

    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.grid(axis="x", color=INK, alpha=0.08, linewidth=0.8)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(outpath, dpi=200, bbox_inches="tight", facecolor=CARD)
    plt.close(fig)
    print(f"wrote {outpath}")


def main():
    setup_rc()
    out = Path(__file__).parent
    cross_attack(out / "robust_fig2_cross_attack.png")


if __name__ == "__main__":
    main()
