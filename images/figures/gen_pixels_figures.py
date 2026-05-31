"""
Figures for projects/from-pixels-to-precision.html.
Cream paper aesthetic, matches gen_cgm_figures.py.
Outputs:
  pixels_fig2_unet.png      U-Net encoder/decoder with skip connections
  pixels_fig3_latency.png   per-frame latency, frame budget context
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

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
# FIG 2 — U-Net: encoder, decoder, skip connections
# =====================================================================
def fig_unet():
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    # depths 0..3, 0 = full res, 3 = bottleneck. Encoder uses levels 0..2 on
    # the left column, decoder uses levels 0..2 on the right column, and a
    # single bottleneck box sits centered between them at level 3.
    enc_x = [1.0, 2.6, 4.2]
    dec_x = [7.8, 9.4, 11.0]
    bottleneck_x = 6.0
    levels_y = [6.0, 4.6, 3.2, 1.8]
    widths   = [1.3, 1.05, 0.82, 0.95]
    heights  = [0.85, 0.70, 0.58, 0.60]

    enc_labels = ["64",  "128", "256"]
    dec_labels = ["256", "128", "64"]

    # encoder column (top 3 levels)
    for i in range(3):
        x = enc_x[i]; y = levels_y[i]; w = widths[i]; h = heights[i]
        ax.add_patch(FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            linewidth=1.1, edgecolor=INK, facecolor=PAPER))
        ax.text(x, y, enc_labels[i], ha="center", va="center",
                fontsize=11, color=INK, family="sans-serif",
                fontweight="bold")

    # bottleneck (single block at level 3)
    bx, by, bw, bh = bottleneck_x, levels_y[3], widths[3], heights[3]
    ax.add_patch(FancyBboxPatch(
        (bx - bw/2, by - bh/2), bw, bh,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        linewidth=1.1, edgecolor=INK, facecolor=PAPER_SUNK))
    ax.text(bx, by, "512", ha="center", va="center",
            fontsize=11, color=INK, family="sans-serif",
            fontweight="bold")
    ax.text(bx, by - bh/2 - 0.30, "bottleneck",
            ha="center", fontsize=9.5, color=INK_FAINT,
            family="serif", style="italic")

    # decoder column (top 3 levels, mirrored)
    for i in range(3):
        x = dec_x[i]
        level = 2 - i
        y = levels_y[level]; w = widths[level]; h = heights[level]
        ax.add_patch(FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            linewidth=1.1, edgecolor=INK,
            facecolor=ACCENT_SOFT if i == 2 else PAPER))
        ax.text(x, y, dec_labels[i], ha="center", va="center",
                fontsize=11, color=INK, family="sans-serif",
                fontweight="bold")

    # encoder down arrows
    for i in range(2):
        x1, x2 = enc_x[i], enc_x[i+1]
        y1, y2 = levels_y[i], levels_y[i+1]
        ax.annotate("", xy=(x2 - widths[i+1]/2 - 0.05, y2),
                    xytext=(x1 + widths[i]/2 + 0.05, y1),
                    arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1.2))
    # encoder last level into bottleneck
    ax.annotate("",
                xy=(bottleneck_x - widths[3]/2 - 0.05, levels_y[3]),
                xytext=(enc_x[2] + widths[2]/2 + 0.05, levels_y[2]),
                arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1.2))

    # bottleneck into decoder first level
    ax.annotate("",
                xy=(dec_x[0] - widths[2]/2 - 0.05, levels_y[2]),
                xytext=(bottleneck_x + widths[3]/2 + 0.05, levels_y[3]),
                arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1.2))

    # decoder up arrows
    for i in range(2):
        level_from = 2 - i
        level_to   = 1 - i
        x1, x2 = dec_x[i], dec_x[i+1]
        y1, y2 = levels_y[level_from], levels_y[level_to]
        ax.annotate("", xy=(x2 - widths[level_to]/2 - 0.05, y2),
                    xytext=(x1 + widths[level_from]/2 + 0.05, y1),
                    arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1.2))

    # skip connections at levels 0,1,2 (horizontal, dashed gold)
    for i in range(3):
        dec_col_for_level_i = 2 - i
        x1 = enc_x[i] + widths[i]/2
        x2 = dec_x[dec_col_for_level_i] - widths[i]/2
        y  = levels_y[i]
        ax.plot([x1, x2], [y, y], linestyle="--",
                color=ACCENT, linewidth=1.6, zorder=0)
        ax.annotate("", xy=(x2 - 0.02, y), xytext=(x2 - 0.5, y),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5))

    # input / output annotations
    ax.text(enc_x[0], levels_y[0] + heights[0]/2 + 0.35,
            "input", ha="center", fontsize=11, color=INK_MUTED,
            family="serif", style="italic")
    ax.text(enc_x[0], levels_y[0] + heights[0]/2 + 0.05,
            "600 × 800 frame", ha="center", fontsize=9.5,
            color=INK_FAINT, family="serif")

    ax.text(dec_x[2], levels_y[0] + heights[0]/2 + 0.35,
            "output", ha="center", fontsize=11, color=INK,
            family="serif", style="italic", fontweight="bold")
    ax.text(dec_x[2], levels_y[0] + heights[0]/2 + 0.05,
            "binary tool mask", ha="center", fontsize=9.5,
            color=INK_FAINT, family="serif")

    # column captions
    ax.text((enc_x[0] + enc_x[2]) / 2, 0.85,
            "Encoder", ha="center", fontsize=12, color=INK,
            family="sans-serif", fontweight="bold")
    ax.text((dec_x[0] + dec_x[2]) / 2, 0.85,
            "Decoder", ha="center", fontsize=12, color=INK,
            family="sans-serif", fontweight="bold")

    # skip legend
    ax.plot([0.6, 1.4], [0.3, 0.3], linestyle="--",
            color=ACCENT, linewidth=1.6)
    ax.text(1.55, 0.3, "skip connection (preserves boundary detail)",
            va="center", fontsize=10, color=INK_MUTED,
            family="serif", style="italic")

    ax.set_title("U-Net. Encoder downsamples to context, decoder upsamples to pixels, skips carry the edges.",
                 fontsize=12, color=INK, family="serif",
                 fontweight="bold", loc="left", pad=14)
    return fig


_save(fig_unet(), "pixels_fig2_unet.png")


# =====================================================================
# FIG 3 — Latency / frame-budget
# =====================================================================
def fig_latency():
    fig, ax = plt.subplots(figsize=(9.5, 3.2))

    per_frame_ms = 120   # <0.12 s
    throughput   = 500   # frames per minute

    ax.barh([0.5], [per_frame_ms], height=0.55,
            color=ACCENT, edgecolor=INK, linewidth=0.9)

    # reference markers
    refs = [(33, "30 FPS video rate"),
            (67, "15 FPS"),
            (200, "5 FPS")]
    for x_ref, label in refs:
        ax.axvline(x_ref, color=INK_FAINT, linestyle=":", linewidth=0.9,
                   zorder=0)
        ax.text(x_ref, 1.18, label, ha="center", va="bottom",
                fontsize=9, color=INK_FAINT, family="serif",
                style="italic", rotation=0)

    ax.text(per_frame_ms + 6, 0.5,
            f"~{per_frame_ms} ms per 600 × 800 frame",
            va="center", fontsize=12.5, color=INK,
            fontweight="bold", family="sans-serif")
    ax.text(per_frame_ms + 6, 0.18,
            f"≈ {throughput} frames per minute on commodity GPU",
            va="center", fontsize=10.5, color=INK_MUTED,
            style="italic", family="serif")

    ax.set_yticks([])
    ax.set_xticks([0, 33, 67, 120, 200, 250])
    ax.set_xticklabels(["0", "33", "67", "120", "200", "250 ms"],
                       family="sans-serif")
    ax.set_xlim(0, 280)
    ax.set_ylim(-0.2, 1.7)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)
    ax.set_facecolor(PAPER_CARD)
    ax.set_title("Inference cost per frame, with video-rate references for context.",
                 fontsize=12, color=INK, family="serif",
                 fontweight="bold", loc="left", pad=18)
    return fig


_save(fig_latency(), "pixels_fig3_latency.png")

print("done.")
