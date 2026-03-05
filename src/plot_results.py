"""Generate publication-ready boxplots of clinical battery scores.

Produces a 4x2 grid of horizontal boxplots (one per battery) showing score
distributions by diagnosis and severity level, with expected high-scoring
diagnoses highlighted in red. Formatted for Nature Medicine (180mm wide,
Arial font, panel labels a-g).
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from run_config import SCORED_RESULTS, PUB_FIGURE_PDF, PUB_FIGURE_PNG

# Constants
INPUT_FILE = str(SCORED_RESULTS)
OUTPUT_PDF = str(PUB_FIGURE_PDF)
OUTPUT_PNG = str(PUB_FIGURE_PNG)

SEVERITY_ORDER = ["Mild", "Moderate", "Severe"]
RED_PALETTE = ["#fcbba1", "#ef3b2c", "#67000d"]

# Battery display order (grouped by domain)
BATTERY_ORDER = ["PHQ-9", "GAD-7", "OCI-R", "PCL-5", "MDQ", "PQ-16", "EDE-Q"]

DIAGNOSIS_ABBREV = {
    "Frontotemporal Dementia (Behavioral Variant)": "FTD",
    "Post-Traumatic Stress Disorder": "PTSD",
    "Obsessive-Compulsive Disorder": "OCD",
    "Alcohol-Induced Mood Disorder": "Alcohol Mood",
    "Generalized Anxiety Disorder": "GAD",
    "Parkinson's Disease Dementia": "Parkinson's",
    "Major Depressive Disorder": "MDD",
    "Binge Eating Disorder": "Binge Eating",
    "Alzheimer's Disease": "Alzheimer's",
    "Bipolar I Disorder": "Bipolar I",
    "Anorexia Nervosa": "Anorexia",
    "Bulimia Nervosa": "Bulimia",
    "Schizophrenia": "Schizophrenia",
}

# Expected high scorers for each battery (highlighted in red on y-axis)
EXPECTED_HIGH = {
    "PHQ-9": ["MDD", "Bipolar I", "Alcohol Mood"],
    "GAD-7": ["GAD", "PTSD", "Alcohol Mood"],
    "OCI-R": ["OCD"],
    "PCL-5": ["PTSD"],
    "MDQ": ["Bipolar I"],
    "PQ-16": ["Schizophrenia", "Parkinson's", "FTD"],
    "EDE-Q": ["Anorexia", "Bulimia", "Binge Eating"],
}


def plot_results():
    """Create and save the main results figure."""
    df = pd.read_csv(INPUT_FILE)

    # Apply abbreviations
    df["Diagnosis"] = df["Diagnosis"].replace(DIAGNOSIS_ABBREV)

    # --- Global style ---
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 6,
        "axes.labelsize": 7,
        "axes.titlesize": 8,
        "xtick.labelsize": 6,
        "ytick.labelsize": 3.5,
        "legend.fontsize": 6,
        "legend.title_fontsize": 7,
    })
    sns.set_theme(style="whitegrid", rc={
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "grid.linewidth": 0.4,
        "axes.linewidth": 0.5,
    })

    # --- Figure setup: 180mm wide, 4x2 grid ---
    fig_width = 7.87  # 200mm in inches — extra room for y-labels
    fig_height = 11.5  # compact rows
    fig = plt.figure(figsize=(fig_width, fig_height))
    gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.40, wspace=0.55)

    for i, battery in enumerate(BATTERY_ORDER):
        row, col = divmod(i, 2)
        ax = fig.add_subplot(gs[row, col])
        data = df[df["Battery"] == battery]

        # Sort diagnoses by median severe score (descending)
        severe_data = data[data["Severity"] == "Severe"]
        if not severe_data.empty:
            order = (severe_data.groupby("Diagnosis")["Score"]
                     .median().sort_values(ascending=False).index)
        else:
            order = (data.groupby("Diagnosis")["Score"]
                     .median().sort_values(ascending=False).index)

        # Boxplot
        sns.boxplot(
            data=data, x="Score", y="Diagnosis", hue="Severity",
            hue_order=SEVERITY_ORDER, order=order, palette=RED_PALETTE,
            ax=ax, orient="h", showfliers=False, linewidth=0.5,
            boxprops={"alpha": 0.7}, medianprops={"linewidth": 0.8},
            whiskerprops={"linewidth": 0.5}, capprops={"linewidth": 0.5},
        )

        # Stripplot for data transparency
        sns.stripplot(
            data=data, x="Score", y="Diagnosis", hue="Severity",
            hue_order=SEVERITY_ORDER, order=order, palette=RED_PALETTE,
            ax=ax, orient="h", dodge=True, alpha=0.35, size=1.5,
            jitter=True, linewidth=0, legend=False,
        )

        # Panel title and labels
        ax.set_title(battery, fontweight="bold", pad=4)
        ax.set_ylabel("")
        ax.set_xlabel("Score")
        ax.tick_params(axis="y", pad=2)

        # Highlight expected high scorers on y-axis
        expected = EXPECTED_HIGH.get(battery, [])
        for tick_label in ax.get_yticklabels():
            if tick_label.get_text() in expected:
                tick_label.set_color("#d62728")
                tick_label.set_fontweight("bold")

        # Remove per-panel legend
        legend = ax.get_legend()
        if legend:
            legend.remove()

    # --- Shared legend in the 8th cell (bottom-right) ---
    ax_legend = fig.add_subplot(gs[3, 1])
    ax_legend.axis("off")

    handles = [
        mpatches.Patch(facecolor=RED_PALETTE[i], edgecolor="gray",
                       linewidth=0.5, alpha=0.7, label=SEVERITY_ORDER[i])
        for i in range(3)
    ]
    ax_legend.legend(
        handles=handles, title="Severity", loc="center",
        frameon=True, edgecolor="0.8", fancybox=False,
        fontsize=11, title_fontsize=12, handlelength=2.5, handleheight=1.5,
        borderpad=1.2, labelspacing=1.0,
    )

    # --- Save ---
    fig.savefig(OUTPUT_PDF, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUTPUT_PNG, dpi=600, bbox_inches="tight", pad_inches=0.02)
    print(f"Saved: {OUTPUT_PDF}")
    print(f"Saved: {OUTPUT_PNG}")
    plt.close(fig)


if __name__ == "__main__":
    plot_results()
