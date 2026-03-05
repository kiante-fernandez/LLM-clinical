"""Score raw simulation responses using standard clinical scoring rubrics.

Maps text responses to numeric values for each battery and computes total
scores (sum for most batteries, subscale averages for EDE-Q).
"""

import pandas as pd
import numpy as np

from run_config import SIMULATION_RESULTS, SCORED_RESULTS

# Constants
INPUT_FILE = str(SIMULATION_RESULTS)
OUTPUT_FILE = str(SCORED_RESULTS)

# Scoring maps: response text -> numeric value
phq_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
gad_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
ocir_map = {"Not at all": 0, "A little": 1, "Moderately": 2, "A lot": 3, "Extremely": 4}
pcl5_map = {"Not at all": 0, "A little bit": 1, "Moderately": 2, "Quite a bit": 3, "Extremely": 4}
mdq_map = {"Yes": 1, "No": 0}
pq16_map = {"True": 1, "False": 0}
edeq_att_map = {"Not at all": 0, "Slightly": 1, "Moderately": 2, "Markedly": 3, "Short period": 4, "Long period": 5, "Every day": 6}

# EDE-Q frequency items: 7 bins mapping to 0-6
edeq_freq_map = {
    "0 days": 0, "1-5 days": 1, "6-12 days": 2, "13-15 days": 3,
    "16-22 days": 4, "23-27 days": 5, "Every day": 6
}

# EDE-Q attitudinal items: 7-point scale (0-6) with labeled anchors
edeq_att_map_sim = {
    "Not at all (0)": 0, "1": 1, "Slightly (2)": 2, "3": 3,
    "Moderately (4)": 4, "5": 5, "Markedly (6)": 6
}

# EDE-Q guilt/proportion scale (Q20): 7-point
edeq_guilt_map = {
    "None of the times": 0, "A few of the times": 1, "Less than half": 2,
    "Half of the times": 3, "More than half": 4, "Most of the time": 5, "Every time": 6
}


def get_score_value(battery, q_id, response):
    """Map a raw text response to its numeric score for the given battery."""
    try:
        if battery == "PHQ-9": return phq_map.get(response, 0)
        if battery == "GAD-7": return gad_map.get(response, 0)
        if battery == "OCI-R": return ocir_map.get(response, 0)
        if battery == "PCL-5": return pcl5_map.get(response, 0)
        if battery == "MDQ": 
            # Only first 13 items count for the score
            if int(q_id.split('_')[1]) <= 13:
                return mdq_map.get(response, 0)
            return 0
        if battery == "PQ-16": return pq16_map.get(response, 0)
        if battery == "EDE-Q":
            if response in edeq_freq_map: return edeq_freq_map[response]
            if response in edeq_att_map_sim: return edeq_att_map_sim[response]
            if response in edeq_guilt_map: return edeq_guilt_map[response]
            # Fallback for text responses (frequencies) - try to parse int
            try:
                return int(response)
            except:
                return 0
        return 0
    except:
        return 0

def calculate_edeq_subscales(df_persona):
    """Compute EDE-Q global score as the mean of four subscale averages.

    Subscale definitions follow EDE-Q 6.0 (Fairburn & Beglin, 2008).
    Item 8 appears in both Shape Concern and Weight Concern per standard scoring.
    """
    restraint_items = [f"EDEQ_{i}" for i in range(1, 6)]
    eating_concern_items = ["EDEQ_7", "EDEQ_9", "EDEQ_19", "EDEQ_20", "EDEQ_21"]
    shape_concern_items = ["EDEQ_6", "EDEQ_8", "EDEQ_10", "EDEQ_11", "EDEQ_23", "EDEQ_26", "EDEQ_27", "EDEQ_28"]
    weight_concern_items = ["EDEQ_22", "EDEQ_24", "EDEQ_25", "EDEQ_12", "EDEQ_8"]
    
    scores = {}
    for subscale, items in [("Restraint", restraint_items), ("Eating Concern", eating_concern_items), 
                            ("Shape Concern", shape_concern_items), ("Weight Concern", weight_concern_items)]:
        sub_vals = []
        for item in items:
            row = df_persona[df_persona['Question_ID'] == item]
            if not row.empty:
                val = get_score_value("EDE-Q", item, row.iloc[0]['Response_Value'])
                sub_vals.append(val)
        
        if sub_vals:
            scores[subscale] = np.mean(sub_vals)
        else:
            scores[subscale] = 0
            
    global_score = np.mean(list(scores.values())) if scores else 0
    return global_score

def main():
    """Load simulation results, score each battery, and write scored_results.csv."""
    df = pd.read_csv(INPUT_FILE)
    
    results = []
    
    # Group by Persona
    for persona_id, group in df.groupby('Persona_ID'):
        diagnosis = group.iloc[0]['Diagnosis']
        severity = group.iloc[0]['Severity']
        
        # Calculate scores for each battery
        for battery, batt_group in group.groupby('Battery'):
            score = 0
            
            if battery == "EDE-Q":
                score = calculate_edeq_subscales(batt_group)
            else:
                # Simple Sum
                for _, row in batt_group.iterrows():
                    score += get_score_value(battery, row['Question_ID'], row['Response_Value'])
            
            results.append({
                "Persona_ID": persona_id,
                "Diagnosis": diagnosis,
                "Severity": severity,
                "Battery": battery,
                "Score": score
            })
            
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Scoring complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
