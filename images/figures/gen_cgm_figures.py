"""
Generates 4 figures for projects/cgm-on-chip.html.
Cream paper aesthetic: ink #1d1a16 on paper #f3ece0, gold accent #b18639.
All figures saved as PNG at 2x retina to images/figures/.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------- Palette ----------
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

# ---------- Global style ----------
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
# FIG 1 (architecture) — clean stack, no center arrow, generous gutters
# =====================================================================
def fig_architecture():
    # Single-column layered stack. Clean breathing room, no chrome.
    fig, ax = plt.subplots(figsize=(10, 6.8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10)
    ax.axis("off")

    title_y = 9.35
    ax.text(0.0, title_y, "Built from primitives.",
            fontsize=22, fontweight="bold", color=INK,
            family="sans-serif")
    ax.text(0.0, title_y - 0.6,
            "Every layer below is something most stacks would simply import.",
            fontsize=12.5, color=INK_MUTED, style="italic",
            family="serif")

    # Reads top-to-bottom: foundation at the bottom, product at the top.
    # `deploy=True` boxes ship to the device (sage tint).
    layers = [
        ("ESP32-S3 firmware",
         "~716 LOC. Serial protocol. Fail-open clinical alarm.", True),
        ("FP32 inference kernel",
         "osdn_inference.h (297 LOC). Allocation-free, stack-only. Same .h file in host and firmware.", True),
        ("Fork-join thread-pool trainer",
         "cgm_train.cpp (~997 LOC). Adam with NaN rejection.", False),
        ("S4D and OSDN models",
         "s4d.cpp (108 LOC), osdn.cpp (218 LOC).", False),
        ("Scalar autograd, complex extension",
         "value.cpp (268 LOC), grad_check.cpp (284 LOC).", False),
        ("C++17 standard library",
         "No PyTorch, no TensorFlow, no Eigen, no BLAS, no OpenMP.", False),
    ]
    # Top → bottom order matches the list; convert to y positions.
    n     = len(layers)
    box_w = 11.5
    box_h = 1.0
    gap   = 0.22
    block_top = 8.4
    box_x = 0.0

    for i, (title, sub, deploy) in enumerate(layers):
        # i = 0 -> top
        y = block_top - i * (box_h + gap) - box_h
        fill = SAGE_BG if deploy else PAPER
        ec   = SAGE_INK if deploy else RULE_STRONG
        title_color = SAGE_INK if deploy else INK
        ax.add_patch(FancyBboxPatch(
            (box_x, y), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.2, edgecolor=ec, facecolor=fill))
        ax.text(box_x + 0.36, y + box_h*0.66, title,
                fontsize=14, fontweight="bold", color=title_color,
                family="sans-serif")
        ax.text(box_x + 0.36, y + box_h*0.26, sub,
                fontsize=10.8, color=INK_MUTED, style="italic",
                family="serif")

    return fig

# Architecture stack figure removed from the page on 2026-05-31. The function
# definition is kept for reference but is no longer rendered.
# _save(fig_architecture(), "fig1_architecture.png")


# =====================================================================
# FIG 2 — 7-channel input the model sees
# =====================================================================
def fig_input_features():
    np.random.seed(7)
    T = 144
    t = np.linspace(0, 12, T)

    glucose = (110
        + 28*np.sin(2*np.pi*t/9.0 + 0.4)
        + 22*np.exp(-((t-3.8)/0.9)**2)*1.4
        - 9*np.tanh((t-9.5)/1.4)
        + np.random.normal(0, 2.0, T))
    dG  = np.gradient(glucose)
    d2G = np.gradient(dG)
    hod = (t + 8) % 24
    sin_tod = np.sin(2*np.pi*hod/24)
    cos_tod = np.cos(2*np.pi*hod/24)
    iob = np.zeros(T)
    for bolus_t, dose in [(3.5, 6.0), (7.2, 4.5)]:
        mask = t >= bolus_t
        iob[mask] += dose * np.exp(-(t[mask]-bolus_t)/1.6)
    cob = np.zeros(T)
    for meal_t, grams in [(3.6, 45.0), (7.3, 30.0)]:
        mask = t >= meal_t
        cob[mask] += grams * np.exp(-(t[mask]-meal_t)/2.2)

    channels = [
        ("Glucose (mg/dL)",        glucose, ACCENT,    True),
        ("ΔGlucose",          dG,      INK,       False),
        ("Δ²Glucose",    d2G,     INK_MUTED, False),
        ("sin(time-of-day)",       sin_tod, SAGE_INK,  False),
        ("cos(time-of-day)",       cos_tod, SAGE_INK,  False),
        ("Insulin-on-board",       iob,     ACCENT,    False),
        ("Carbs-on-board",         cob,     ACCENT,    False),
    ]

    fig, axes = plt.subplots(7, 1, figsize=(9, 6.8), sharex=True,
                             gridspec_kw={"hspace": 0.0})
    for ax, (label, y, color, is_first) in zip(axes, channels):
        ax.plot(t, y, color=color, linewidth=1.5)
        ax.fill_between(t, y, y.min(), color=color, alpha=0.10)
        ax.set_ylabel(label, fontsize=10, color=INK, rotation=0,
                      ha="right", va="center", labelpad=8, family="serif")
        ax.tick_params(left=False, labelleft=False)
        for spine in ("top","right","left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color(RULE)
        ax.set_facecolor(PAPER_CARD)
        if is_first:
            ax.axhline(70, color=INK_FAINT, linestyle=":", linewidth=0.9)
            ax.text(11.85, 72, "70 mg/dL", fontsize=8,
                    color=INK_FAINT, ha="right", style="italic")

    axes[-1].set_xlabel("Time (hours into 12-hour lookback window)",
                        fontsize=11, color=INK_MUTED, family="sans-serif")
    axes[-1].set_xticks(range(0, 13, 2))

    fig.suptitle("Seven channels, 144 samples, one window",
                 fontsize=15, fontweight="bold", color=INK,
                 x=0.5, y=0.99, family="sans-serif")
    return fig

_save(fig_input_features(), "fig2_input_channels.png")


# =====================================================================
# FIG 3 — S4D vs OSDN results (legend pinned outside)
# =====================================================================
def fig_results():
    metrics = ["Val AUROC", "Test AUROC", "Recall @ spec 0.80"]
    s4d_p  = [0.9510, 0.9113, 0.918]
    osdn_p = [0.9220, 0.7669, 0.718]
    s4d_lat,  osdn_lat = 189.8, 236.4

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.6),
                                   gridspec_kw={"width_ratios": [3, 1.1]})
    fig.subplots_adjust(wspace=0.32, top=0.82)

    x = np.arange(len(metrics))
    w = 0.36
    b1 = ax1.bar(x - w/2, s4d_p,  w, color=INK,    label="S4D",
                 edgecolor=INK, linewidth=0.6)
    b2 = ax1.bar(x + w/2, osdn_p, w, color=ACCENT, label="OSDN",
                 edgecolor=INK, linewidth=0.6)
    for b in list(b1) + list(b2):
        v = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, v + 0.012, f"{v:.3f}",
                 ha="center", fontsize=10.5, color=INK,
                 family="sans-serif")
    ax1.set_xticks(x); ax1.set_xticklabels(metrics, family="sans-serif",
                                           fontsize=11)
    ax1.set_ylim(0, 1.10)
    ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax1.set_ylabel("score", color=INK_MUTED, family="sans-serif")
    ax1.set_facecolor(PAPER_CARD)
    ax1.legend(frameon=False, fontsize=11.5,
               ncol=2, loc="upper center",
               bbox_to_anchor=(0.5, 1.16))

    ax2.bar([0], [s4d_lat],  0.55, color=INK,    edgecolor=INK)
    ax2.bar([1], [osdn_lat], 0.55, color=ACCENT, edgecolor=INK)
    for x0, v in [(0, s4d_lat), (1, osdn_lat)]:
        ax2.text(x0, v + 6, f"{v:.1f}", ha="center", fontsize=10.5,
                 color=INK, family="sans-serif")
    ax2.set_xticks([0,1]); ax2.set_xticklabels(["S4D","OSDN"],
                                               family="sans-serif",
                                               fontsize=11)
    ax2.set_ylim(0, max(s4d_lat, osdn_lat)*1.20)
    ax2.set_ylabel("ms / window (host)", color=INK_MUTED,
                   family="sans-serif")
    ax2.set_facecolor(PAPER_CARD)

    fig.suptitle("Same wrapper, same data. Only the recurrent backbone differs.",
                 fontsize=12.5, color=INK, family="serif",
                 fontweight="bold", y=1.01)
    return fig

_save(fig_results(), "fig3_results.png")


# =====================================================================
# FIG 4 — ESP32-S3 footprint with byte text BELOW the bar
# =====================================================================
def fig_footprint():
    fig, ax = plt.subplots(figsize=(9.5, 3.6))

    cats = ["RAM", "Flash"]
    used = [20.1, 8.4]
    used_b = ["65,964 B", "281,161 B"]
    tot_b  = ["327,680 B", "3,342,336 B"]

    # widen y-spacing so the byte-line sits cleanly between bars
    y_positions = np.array([2.0, 0.5])  # RAM on top, Flash below

    bar_h = 0.55
    # Empty (total) bar
    ax.barh(y_positions, [100, 100], height=bar_h,
            color=PAPER_SUNK, edgecolor=RULE_STRONG, linewidth=1.0)
    # Filled portion
    ax.barh(y_positions, used, height=bar_h,
            color=ACCENT, edgecolor=INK, linewidth=0.8)

    for yi, u, ub, tb in zip(y_positions, used, used_b, tot_b):
        # Percentage label right after the gold bar end
        ax.text(u + 1.5, yi, f"{u:.1f}% used", va="center",
                fontsize=12.5, color=INK, fontweight="bold",
                family="sans-serif")
        # Byte-line under the bar, on the paper background
        ax.text(0, yi - bar_h/2 - 0.18,
                f"{ub} of {tb}", va="top", ha="left",
                fontsize=10, color=INK_MUTED, style="italic",
                family="serif")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(cats, fontsize=14, fontweight="bold",
                       family="sans-serif")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%","25%","50%","75%","100%"],
                       family="sans-serif")
    ax.set_xlim(0, 105)
    ax.set_ylim(-0.4, 2.9)
    for s in ("top","right","left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)
    ax.set_facecolor(PAPER_CARD)
    ax.set_title("Full model, full firmware, room to spare",
                 fontsize=13, color=INK, family="serif",
                 fontweight="bold", loc="left", pad=14)
    return fig

_save(fig_footprint(), "fig4_footprint.png")

# Remove old fig5 if present
old5 = os.path.join(OUT_DIR, "fig5_alarm.png")
if os.path.exists(old5):
    os.remove(old5)
    print(f"removed {old5}")

print("done.")
