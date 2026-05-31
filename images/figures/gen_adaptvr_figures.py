"""
Figures for projects/adaptvr.html.
Cream paper aesthetic, matches gen_cgm_figures.py and gen_pixels_figures.py.
Outputs:
  adaptvr_fig2_envelope.png   Top-down safety envelope (spawn zone + overextension boundary)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Circle

PAPER       = "#f3ece0"
PAPER_CARD  = "#f9f3e6"
PAPER_SUNK  = "#ece4d4"
INK         = "#1d1a16"
INK_MUTED   = "#6b6359"
INK_FAINT   = "#8e857a"
RULE        = "#d6cdb9"
RULE_STRONG = "#b8ad96"
ACCENT      = "#b18639"
ACCENT_SOFT = "#e3c98a"
SAGE_BG     = "#d8e4d4"
SAGE_INK    = "#2f4a36"
ROSE        = "#c98686"
ROSE_SOFT   = "#ecc9c9"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

rcParams.update({
    "font.family": "serif",
    "font.serif":  ["EB Garamond", "Georgia", "Times New Roman", "DejaVu Serif"],
    "font.size": 11,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "axes.titlecolor": INK,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 200,
    "savefig.facecolor": PAPER_CARD,
    "figure.facecolor": PAPER_CARD,
    "axes.facecolor":   PAPER_CARD,
})


def _save(fig, name):
    out = os.path.join(OUT_DIR, name)
    fig.savefig(out, bbox_inches="tight", pad_inches=0.3, dpi=200,
                facecolor=PAPER_CARD)
    plt.close(fig)
    print(f"wrote {out}")


# =====================================================================
# FIG 2 — Top-down safety envelope: spawn zone inside overextension boundary
# =====================================================================
def fig_envelope():
    fig, ax = plt.subplots(figsize=(8.5, 6.6))
    ax.set_aspect("equal")

    # Player head at origin (top-down view, "+y forward" convention)
    head_xy = (0.0, 0.0)
    head_r  = 0.085

    # Overextension boundary: a circle of radius 0.65 m around the head.
    overext_r = 0.65
    ax.add_patch(Circle(head_xy, overext_r,
                        facecolor=ROSE_SOFT, edgecolor=ROSE,
                        linewidth=1.4, linestyle="--", alpha=0.55, zorder=1))

    # Spawn zone: a disk of radius 0.9 m, centered 1.2 m forward of the head.
    spawn_center = (0.0, 1.2)
    spawn_r = 0.9
    ax.add_patch(Circle(spawn_center, spawn_r,
                        facecolor=SAGE_BG, edgecolor=SAGE_INK,
                        linewidth=1.4, alpha=0.65, zorder=2))

    # Head marker on top.
    ax.add_patch(Circle(head_xy, head_r,
                        facecolor=INK, edgecolor=INK,
                        linewidth=1.0, zorder=10))
    # Head facing direction (small triangle nose)
    nose_tip = (0.0, head_r + 0.10)
    nose_l   = (-0.05, head_r + 0.01)
    nose_r   = (0.05,  head_r + 0.01)
    ax.add_patch(plt.Polygon([nose_tip, nose_l, nose_r],
                             closed=True, facecolor=INK, edgecolor=INK,
                             zorder=11))

    # Butterfly sample points inside spawn zone. Hand-placed (not random) so
    # they cluster away from the central vertical axis where the distFromHead
    # leader runs, and away from the zoneRadius arrow at y=spawn_center[1].
    bxs = np.array([-0.55, -0.30,  0.30,  0.60,  0.45])
    bys = np.array([ 1.85,  1.55,  1.85,  1.55,  0.85])
    ax.scatter(bxs, bys, s=70, marker="*",
               facecolor=ACCENT, edgecolor=INK, linewidth=0.7, zorder=6)

    # ---- maxReachMeters annotation ----
    # Radius arrow from the head outward to the LEFT (mirrors the zoneRadius
    # arrow which goes outward to the right on the spawn zone). Label sits
    # OUTSIDE the rose circle so it reads against the cream background, not
    # against the rose fill.
    ax.annotate("",
                xy=(-overext_r, 0.0), xytext=(0.0, 0.0),
                arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.4))
    ax.text(-overext_r - 0.05, 0.10, "0.65 m  maxReachMeters",
            ha="right", va="bottom", fontsize=10.5, color=ROSE,
            family="serif", style="italic")

    # ---- distFromHead annotation ----
    # Vertical arrow head -> spawn center, with a horizontal dotted leader out
    # to the right so the label sits OUTSIDE the spawn zone.
    ax.annotate("",
                xy=(0.0, 1.2), xytext=(0.0, head_r + 0.12),
                arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1.1))
    ax.plot([0.0, 1.05], [0.65, 0.65],
            linestyle=":", color=INK_FAINT, linewidth=0.9, zorder=4)
    ax.text(1.08, 0.65, "1.2 m  distFromHead",
            ha="left", va="center", fontsize=10.5, color=INK_MUTED,
            family="serif", style="italic")

    # ---- zoneRadius annotation ----
    # Radius arrow from spawn center outward to the right.
    ax.annotate("",
                xy=(spawn_r, 1.2), xytext=(0.0, 1.2),
                arrowprops=dict(arrowstyle="->", color=SAGE_INK, lw=1.2))
    ax.text(spawn_r/2, 1.32, "0.9 m  zoneRadius",
            ha="center", va="bottom", fontsize=10.5, color=SAGE_INK,
            family="serif", style="italic")

    # Region labels
    ax.text(-spawn_r - 0.10, 1.7, "spawn zone",
            ha="right", va="center", fontsize=11, color=SAGE_INK,
            family="sans-serif", fontweight="bold")
    ax.text(-overext_r - 0.10, -0.30, "safe reach",
            ha="right", va="center", fontsize=11, color=ROSE,
            family="sans-serif", fontweight="bold")

    # Player label below the head, clear of the maxReachMeters arrow
    ax.text(0.0, -0.22, "player",
            ha="center", va="top", fontsize=10, color=INK,
            family="serif", style="italic")

    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-0.8, 2.5)
    ax.axis("off")

    ax.set_title("Top-down view. Spawn zone sits at the far edge of safe reach by design.",
                 fontsize=12.5, color=INK, family="serif",
                 fontweight="bold", loc="left", pad=14)
    return fig


_save(fig_envelope(), "adaptvr_fig2_envelope.png")

print("done.")
