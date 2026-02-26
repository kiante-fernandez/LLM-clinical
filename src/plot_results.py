"""Generate publication-ready boxplots of clinical battery scores.

Produces a grid of horizontal boxplots (one per battery) showing score
distributions by diagnosis and severity level, with expected high-scoring
diagnoses highlighted in red.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# Constants
INPUT_FILE = "../data/scored_results.csv"
OUTPUT_FILE = "../figures/publication_ready_plot_v5.png"
SEVERITY_ORDER = ["Mild", "Moderate", "Severe"]
RED_PALETTE = ["#fcbba1", "#ef3b2c", "#67000d"]


def plot_results():
    """Create and save the main results figure."""
    df = pd.read_csv(INPUT_FILE)

    # Expected high scorers for each battery (highlighted in red on y-axis)
    expected_high = {
        "PHQ-9": ["Major Depressive Disorder", "Bipolar I Disorder", "Alcohol-Induced Mood Disorder"],
        "GAD-7": ["Generalized Anxiety Disorder", "Post-Traumatic Stress Disorder", "Alcohol-Induced Mood Disorder"],
        "OCI-R": ["Obsessive-Compulsive Disorder"],
        "PCL-5": ["Post-Traumatic Stress Disorder"],
        "MDQ": ["Bipolar I Disorder"],
        "PQ-16": ["Schizophrenia", "Parkinson's Disease Dementia", "Frontotemporal Dementia (Behavioral Variant)"],
        "EDE-Q": ["Anorexia Nervosa", "Bulimia Nervosa", "Binge Eating Disorder"]
    }
    
    batteries = df['Battery'].unique()
    n_batteries = len(batteries)
    n_cols = 3
    n_rows = math.ceil(n_batteries / n_cols)
    
    # Set up the plot style
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 10 * n_rows), constrained_layout=True)
    axes = axes.flatten()
    
    for i, battery in enumerate(batteries):
        ax = axes[i]
        data = df[df['Battery'] == battery]
        
        # Calculate median score for 'Severe' cases to sort
        severe_data = data[data['Severity'] == 'Severe']
        if not severe_data.empty:
            order = severe_data.groupby('Diagnosis')['Score'].median().sort_values(ascending=False).index
        else:
            order = data.groupby('Diagnosis')['Score'].median().sort_values(ascending=False).index
        
        # Plot Boxplot
        sns.boxplot(
            data=data,
            x="Score",
            y="Diagnosis",
            hue="Severity",
            hue_order=SEVERITY_ORDER,
            order=order,
            palette=RED_PALETTE,
            ax=ax,
            orient="h",
            showfliers=False,
            boxprops={'alpha': 0.7}
        )
        
        # Plot Individual Points
        sns.stripplot(
            data=data,
            x="Score",
            y="Diagnosis",
            hue="Severity",
            hue_order=SEVERITY_ORDER,
            order=order,
            palette=RED_PALETTE, # Match the box colors
            ax=ax,
            orient="h",
            dodge=True,
            alpha=0.5,
            size=3,
            jitter=True,
            linewidth=0.5,
            edgecolor='gray' # Add slight edge to make points pop
        )
        
        ax.set_title(battery, fontweight='bold', fontsize=16)
        ax.set_ylabel("")
        ax.set_xlabel("Score", fontsize=12)
        ax.tick_params(axis='y', labelsize=11)
        
        # Highlight expected high scorers
        expected = expected_high.get(battery, [])
        for tick_label in ax.get_yticklabels():
            if tick_label.get_text() in expected:
                tick_label.set_color("#d62728") # Red
                tick_label.set_fontweight("bold")
            else:
                tick_label.set_color("black")
                
        # Handle Legend: Only show for the first plot, OUTSIDE
        if i == 0:
            # Get handles and labels, keep only the first 3 (Severity levels)
            handles, labels = ax.get_legend_handles_labels()
            # Place legend outside the plot to the right
            ax.legend(handles[:3], labels[:3], title="Severity", loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
        else:
            if ax.get_legend():
                ax.get_legend().remove()

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
        
    fig.suptitle('Clinical Simulation Results: Scores by Diagnosis and Severity (Sorted by Severe Score)', fontsize=20, fontweight='bold')
    
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_results()
