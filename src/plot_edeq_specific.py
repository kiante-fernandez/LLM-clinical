"""EDE-Q item-level analysis for binge eating frequency.

Plots boxplots for EDE-Q items 13 (binge eating episodes) and 14
(loss of control) to examine eating disorder specificity.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

from run_config import SIMULATION_RESULTS, EDEQ_PLOT

# Constants
INPUT_FILE = str(SIMULATION_RESULTS)
OUTPUT_FILE = str(EDEQ_PLOT)
SEVERITY_ORDER = ["Mild", "Moderate", "Severe"]
RED_PALETTE = ["#fcbba1", "#ef3b2c", "#67000d"]
TARGET_QUESTIONS = ["EDEQ_13", "EDEQ_14"]
QUESTION_TITLES = {
    "EDEQ_13": "Q13: Frequency of Binge Eating (Episodes)",
    "EDEQ_14": "Q14: Loss of Control (Episodes)",
}
ED_DIAGNOSES = ["Anorexia Nervosa", "Bulimia Nervosa", "Binge Eating Disorder"]


def parse_numeric_response(val):
    """Extract the first numeric value from a string response."""
    try:
        # If it's already a number (int/float), return it
        if isinstance(val, (int, float)):
            return float(val)
        
        # If string, look for digits
        # This handles "5 times", "About 10", "0", etc.
        match = re.search(r'\d+', str(val))
        if match:
            return float(match.group())
        return 0.0 # Default to 0 if no number found
    except:
        return 0.0

def plot_edeq_specific():
    """Create and save the EDE-Q item-level analysis figure."""
    df = pd.read_csv(INPUT_FILE)

    df_subset = df[df['Question_ID'].isin(TARGET_QUESTIONS)].copy()
    df_subset['Numeric_Score'] = df_subset['Response_Value'].apply(parse_numeric_response)
    df_subset['Question_Title'] = df_subset['Question_ID'].map(QUESTION_TITLES)

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)
    
    # Create 2 subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(20, 12), constrained_layout=True)
    
    for i, q_id in enumerate(TARGET_QUESTIONS):
        ax = axes[i]
        data = df_subset[df_subset['Question_ID'] == q_id]
        
        # Sort logic: Median score of 'Severe' group
        severe_data = data[data['Severity'] == 'Severe']
        if not severe_data.empty:
            order = severe_data.groupby('Diagnosis')['Numeric_Score'].median().sort_values(ascending=False).index
        else:
            order = data.groupby('Diagnosis')['Numeric_Score'].median().sort_values(ascending=False).index
            
        # Boxplot
        sns.boxplot(
            data=data,
            x="Numeric_Score",
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

        # Stripplot
        sns.stripplot(
            data=data,
            x="Numeric_Score",
            y="Diagnosis",
            hue="Severity",
            hue_order=SEVERITY_ORDER,
            order=order,
            palette=RED_PALETTE,
            ax=ax,
            orient="h",
            dodge=True,
            alpha=0.5,
            size=3,
            jitter=True,
            linewidth=0.5,
            edgecolor='gray'
        )
        
        ax.set_title(QUESTION_TITLES[q_id], fontweight='bold', fontsize=16)
        ax.set_xlabel("Number of Times (Past 28 Days)", fontsize=12)
        ax.set_ylabel("")
        ax.tick_params(axis='y', labelsize=11)
        
        for tick_label in ax.get_yticklabels():
            if tick_label.get_text() in ED_DIAGNOSES:
                tick_label.set_color("#d62728")
                tick_label.set_fontweight("bold")
        
        if i == 1:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[:3], labels[:3], title="Severity", loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
        else:
            if ax.get_legend():
                ax.get_legend().remove()

    fig.suptitle('EDE-Q Specific Item Analysis: Binge Eating Frequency', fontsize=20, fontweight='bold')
    
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_edeq_specific()
