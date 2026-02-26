"""Clinical assessment battery definitions.

Defines 7 validated psychiatric instruments (PHQ-9, GAD-7, OCI-R, PCL-5, MDQ,
PQ-16, EDE-Q) with their items and response options. Each battery is a list of
question dicts consumed by the simulation engine.
"""

# Response option scales
phq_options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
gad_options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
ocir_options = ["Not at all", "A little", "Moderately", "A lot", "Extremely"]
pcl5_options = ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]
mdq_options = ["Yes", "No"]
pq16_options = ["True", "False"] # Followed by distress if true, but simplified for simulation
edeq_freq_options = ["0 days", "1-5 days", "6-12 days", "13-15 days", "16-22 days", "23-27 days", "Every day"]
edeq_att_options = ["Not at all", "Slightly", "Moderately", "Markedly"]

# --- Depression (PHQ-9) ---
# Source: Kroenke, K., Spitzer, R. L., & Williams, J. B. (2001). The PHQ-9: validity of a brief depression severity measure. Journal of general internal medicine, 16(9), 606-613.
phq9 = [
    {"question_id": "PHQ9_1", "question_text": "Little interest or pleasure in doing things", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_2", "question_text": "Feeling down, depressed, or hopeless", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_3", "question_text": "Trouble falling or staying asleep, or sleeping too much", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_4", "question_text": "Feeling tired or having little energy", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_5", "question_text": "Poor appetite or overeating", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_6", "question_text": "Feeling bad about yourself - or that you are a failure or have let yourself or your family down", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_7", "question_text": "Trouble concentrating on things, such as reading the newspaper or watching television", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_8", "question_text": "Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual", "question_type": "multiple_choice", "question_response_options": phq_options},
    {"question_id": "PHQ9_9", "question_text": "Thoughts that you would be better off dead or of hurting yourself in some way", "question_type": "multiple_choice", "question_response_options": phq_options},
]

# --- Anxiety (GAD-7) ---
# Source: Spitzer, R. L., Kroenke, K., Williams, J. B., & Löwe, B. (2006). A brief measure for assessing generalized anxiety disorder: the GAD-7. Archives of internal medicine, 166(10), 1092-1097.
gad7 = [
    {"question_id": "GAD7_1", "question_text": "Feeling nervous, anxious or on edge", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_2", "question_text": "Not being able to stop or control worrying", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_3", "question_text": "Worrying too much about different things", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_4", "question_text": "Trouble relaxing", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_5", "question_text": "Being so restless that it is hard to sit still", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_6", "question_text": "Becoming easily annoyed or irritable", "question_type": "multiple_choice", "question_response_options": gad_options},
    {"question_id": "GAD7_7", "question_text": "Feeling afraid as if something awful might happen", "question_type": "multiple_choice", "question_response_options": gad_options},
]

# --- OCD (OCI-R) ---
# Source: Foa, E. B., et al. (2002). The Obsessive-Compulsive Inventory: development and validation of a short version. Psychological assessment, 14(4), 485.
ocir = [
    {"question_id": "OCIR_1", "question_text": "I have saved up so many things that they get in the way.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_2", "question_text": "I check things more often than necessary.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_3", "question_text": "I get upset if objects are not arranged properly.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_4", "question_text": "I feel compelled to count while I am doing things.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_5", "question_text": "I find it difficult to touch an object when I know it has been touched by strangers or certain people.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_6", "question_text": "I find it difficult to control my own thoughts.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_7", "question_text": "I collect things I don't need.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_8", "question_text": "I repeatedly check doors, windows, drawers, etc.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_9", "question_text": "I get upset if others change the way I have arranged things.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_10", "question_text": "I feel I have to repeat certain numbers.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_11", "question_text": "I sometimes have to wash or clean myself simply because I feel contaminated.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_12", "question_text": "I am upset by unpleasant thoughts that come into my mind against my will.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_13", "question_text": "I avoid throwing things away because I am afraid I might need them later.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_14", "question_text": "I repeatedly check gas and water taps and light switches after turning them off.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_15", "question_text": "I need things to be arranged in a particular order.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_16", "question_text": "I feel that there are good and bad numbers.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_17", "question_text": "I wash my hands more often and longer than necessary.", "question_type": "multiple_choice", "question_response_options": ocir_options},
    {"question_id": "OCIR_18", "question_text": "I frequently get nasty thoughts and have difficulty in getting rid of them.", "question_type": "multiple_choice", "question_response_options": ocir_options},
]

# --- PTSD (PCL-5) ---
# Source: Weathers, F. W., et al. (2013). The PTSD Checklist for DSM-5 (PCL-5). National Center for PTSD.
pcl5 = [
    {"question_id": "PCL5_1", "question_text": "Repeated, disturbing, and unwanted memories of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_2", "question_text": "Repeated, disturbing dreams of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_3", "question_text": "Suddenly feeling or acting as if the stressful experience were actually happening again?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_4", "question_text": "Feeling very upset when something reminded you of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_5", "question_text": "Having strong physical reactions when something reminded you of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_6", "question_text": "Avoiding memories, thoughts, or feelings related to the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_7", "question_text": "Avoiding external reminders of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_8", "question_text": "Trouble remembering important parts of the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_9", "question_text": "Having strong negative beliefs about yourself, other people, or the world?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_10", "question_text": "Blaming yourself or someone else for the stressful experience?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_11", "question_text": "Strong negative feelings such as fear, horror, anger, guilt, or shame?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_12", "question_text": "Loss of interest in activities you once enjoyed?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_13", "question_text": "Feeling distant or cut off from other people?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_14", "question_text": "Trouble experiencing positive feelings?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_15", "question_text": "Irritable behavior, angry outbursts, or acting aggressively?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_16", "question_text": "Taking too many risks or doing things that could cause you harm?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_17", "question_text": "Being 'on guard', watchful, or easily startled?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_18", "question_text": "Feeling jumpy or easily startled?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_19", "question_text": "Having difficulty concentrating?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
    {"question_id": "PCL5_20", "question_text": "Trouble falling or staying asleep?", "question_type": "multiple_choice", "question_response_options": pcl5_options},
]

# --- Bipolar (MDQ) ---
# Source: Hirschfeld, R. M., et al. (2000). Development and validation of a screening instrument for bipolar spectrum disorder: the Mood Disorder Questionnaire. American Journal of Psychiatry, 157(11), 1873-1875.
mdq = [
    {"question_id": "MDQ_1", "question_text": "You felt so good or so hyper that other people thought you were not your normal self or you were so hyper that you got into trouble?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_2", "question_text": "You were so irritable that you shouted at people or started fights or arguments?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_3", "question_text": "You felt much more self-confident than usual?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_4", "question_text": "You got much less sleep than usual and found you didn't really miss it?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_5", "question_text": "You were much more talkative or spoke much faster than usual?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_6", "question_text": "Thoughts raced through your head or you couldn't slow your mind down?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_7", "question_text": "You were so easily distracted by things around you that you had trouble concentrating or staying on track?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_8", "question_text": "You had much more energy than usual?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_9", "question_text": "You were much more active or did many more things than usual?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_10", "question_text": "You were much more social or outgoing than usual, for example, you telephoned friends in the middle of the night?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_11", "question_text": "You were much more interested in sex than usual?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_12", "question_text": "You did things that were unusual for you or that other people might have thought were excessive, foolish, or risky?", "question_type": "multiple_choice", "question_response_options": mdq_options},
    {"question_id": "MDQ_13", "question_text": "Spending money got you or your family in trouble?", "question_type": "multiple_choice", "question_response_options": mdq_options},
]

# --- Psychosis (PQ-16) ---
# Source: Ising, H. K., et al. (2012). The validity of the 16-item Prodromal Questionnaire (PQ-16)... Schizophrenia bulletin, 38(6), 1288-1296.
pq16 = [
    {"question_id": "PQ16_1", "question_text": "I feel uninterested in the things I used to enjoy.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_2", "question_text": "I often seem to live through events exactly as they happened before (déjà vu).", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_3", "question_text": "I hear sounds or voices that other people can't hear.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_4", "question_text": "I feel that things I see on TV or read in magazines have a special meaning for me.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_5", "question_text": "I have felt that I am not myself, or that I am strange or unreal.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_6", "question_text": "When I look at a person, or look at myself in a mirror, I have seen the face change right before my eyes.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_7", "question_text": "I have had the experience of thoughts being put into my head that were not my own.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_8", "question_text": "I have had the experience of thoughts being taken out of my head by some outside force.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_9", "question_text": "I have felt that strangers are talking about me or making fun of me.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_10", "question_text": "I have felt that people are watching me or spying on me.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_11", "question_text": "I have seen things that other people cannot see.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_12", "question_text": "I have had periods of confusion when I wasn't sure what was real and what was imaginary.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_13", "question_text": "I have difficulty organizing my thoughts.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_14", "question_text": "I have felt that I was a special person or that I had special powers.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_15", "question_text": "I have felt that my mind was controlled by an outside force.", "question_type": "multiple_choice", "question_response_options": pq16_options},
    {"question_id": "PQ16_16", "question_text": "I feel that parts of my body have changed in some way, or that parts of my body are working differently than before.", "question_type": "multiple_choice", "question_response_options": pq16_options},
]

# --- Eating Disorders (EDE-Q 6.0) ---
# Source: Fairburn, C. G., & Beglin, S. J. (2008). Eating Disorder Examination Questionnaire (EDE-Q 6.0). In Cognitive Behavior Therapy and Eating Disorders.
edeq = [
    # Attitudinal (0-6 scale)
    {"question_id": "EDEQ_1", "question_text": "Have you been deliberately trying to limit the amount of food you eat to influence your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_2", "question_text": "Have you gone for long periods of time (8 waking hours or more) without eating anything at all in order to influence your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_3", "question_text": "Have you tried to exclude from your diet any foods that you like in order to influence your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_4", "question_text": "Have you tried to follow definite rules regarding your eating (for example, a calorie limit) in order to influence your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_5", "question_text": "Have you had a definite desire to have an empty stomach with the aim of influencing your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_6", "question_text": "Have you had a clear desire to have a totally flat stomach?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_7", "question_text": "Has thinking about food, eating or calories made it very difficult to concentrate on things you are interested in?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_8", "question_text": "Has thinking about shape or weight made it very difficult to concentrate on things you are interested in?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_9", "question_text": "Have you had a definite fear of losing control over eating?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_10", "question_text": "Have you had a definite fear that you might gain weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_11", "question_text": "Have you felt fat?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    {"question_id": "EDEQ_12", "question_text": "Have you had a strong desire to lose weight?", "question_type": "multiple_choice", "question_response_options": edeq_freq_options},
    # Behavioral (Frequency)
    {"question_id": "EDEQ_13", "question_text": "Over the past 28 days, how many times have you eaten what other people would regard as an unusually large amount of food?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_14", "question_text": "On how many of these times did you have a sense of having lost control over your eating?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_15", "question_text": "Over the past 28 days, on how many DAYS have such episodes of overeating occurred?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_16", "question_text": "Over the past 28 days, how many times have you made yourself sick (vomit) as a means of controlling your shape or weight?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_17", "question_text": "Over the past 28 days, how many times have you taken laxatives as a means of controlling your shape or weight?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_18", "question_text": "Over the past 28 days, how many times have you exercised in a 'driven' or 'compulsive' way as a means of controlling your weight, shape or amount of fat?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_19", "question_text": "Over the past 28 days, on how many days have you eaten in secret?", "question_type": "text", "question_response_options": []},
    {"question_id": "EDEQ_20", "question_text": "How many of the times you have eaten, have you had guilt because it can affect your shape or weight?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_21", "question_text": "Over the past 28 days, how concerned have you been about other people seeing you eat?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    # Shape/Weight Concern
    {"question_id": "EDEQ_22", "question_text": "Has your weight influenced how you think about (judge) yourself as a person?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_23", "question_text": "Has your shape influenced how you think about (judge) yourself as a person?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_24", "question_text": "How much would it have upset you if you had been asked to weigh yourself once a week for the next four weeks?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_25", "question_text": "How dissatisfied have you been with your weight?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_26", "question_text": "How dissatisfied have you been with your shape?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_27", "question_text": "How uncomfortable have you felt seeing your body?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
    {"question_id": "EDEQ_28", "question_text": "How uncomfortable have you felt about others seeing your shape or figure?", "question_type": "multiple_choice", "question_response_options": edeq_att_options},
]

batteries = {
    "PHQ-9": phq9,
    "GAD-7": gad7,
    "OCI-R": ocir,
    "PCL-5": pcl5,
    "MDQ": mdq,
    "PQ-16": pq16,
    "EDE-Q": edeq
}
