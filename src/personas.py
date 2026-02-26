"""Synthetic clinical persona generation.

Generates 2,028 unique personas by combining 13 diagnostic profiles with
demographic factors (age, gender, education, political affiliation, severity).
Each persona is a dictionary used as input to the simulation engine.
"""

import itertools

# Clinical Profiles (13 Diagnoses)
clinical_profiles = [
    {
        "code": "GAD",
        "diagnosis": "Generalized Anxiety Disorder",
        "symptoms": ["excessive worry", "restlessness", "difficulty concentrating", "muscle tension"]
    },
    {
        "code": "OCD",
        "diagnosis": "Obsessive-Compulsive Disorder",
        "symptoms": ["intrusive thoughts about contamination", "compulsive hand-washing", "checking locks", "distress when rituals are interrupted"]
    },
    {
        "code": "PTSD",
        "diagnosis": "Post-Traumatic Stress Disorder",
        "symptoms": ["flashbacks", "nightmares", "hypervigilance", "avoidance of triggers related to combat"]
    },
    {
        "code": "MDD",
        "diagnosis": "Major Depressive Disorder",
        "symptoms": ["persistent sadness", "anhedonia", "fatigue", "insomnia", "feelings of worthlessness"]
    },
    {
        "code": "Bipolar",
        "diagnosis": "Bipolar I Disorder",
        "symptoms": ["periods of mania", "inflated self-esteem", "decreased need for sleep", "depressive episodes"]
    },
    {
        "code": "SubstanceMood",
        "diagnosis": "Alcohol-Induced Mood Disorder",
        "symptoms": ["depressive symptoms during withdrawal", "irritability", "anxiety", "craving"]
    },
    {
        "code": "Schizophrenia",
        "diagnosis": "Schizophrenia",
        "symptoms": ["auditory hallucinations", "paranoid delusions", "disorganized speech", "flat affect"]
    },
    {
        "code": "Alzheimers",
        "diagnosis": "Alzheimer's Disease",
        "symptoms": ["short-term memory loss", "confusion about time/place", "difficulty finding words", "getting lost"]
    },
    {
        "code": "Parkinsons",
        "diagnosis": "Parkinson's Disease Dementia",
        "symptoms": ["resting tremor", "bradykinesia", "visual hallucinations", "executive dysfunction", "slowed thinking"]
    },
    {
        "code": "FTD",
        "diagnosis": "Frontotemporal Dementia (Behavioral Variant)",
        "symptoms": ["disinhibition", "socially inappropriate behavior", "apathy", "loss of empathy", "compulsive behaviors"]
    },
    {
        "code": "Anorexia",
        "diagnosis": "Anorexia Nervosa",
        "symptoms": ["intense fear of gaining weight", "distorted body image", "severe restriction of food intake", "amenorrhea"]
    },
    {
        "code": "Bulimia",
        "diagnosis": "Bulimia Nervosa",
        "symptoms": ["recurrent binge eating", "compensatory purging", "self-evaluation unduly influenced by body shape"]
    },
    {
        "code": "BingeEating",
        "diagnosis": "Binge Eating Disorder",
        "symptoms": ["eating large amounts rapidly", "eating until uncomfortably full", "eating alone due to embarrassment", "feeling disgusted with oneself"]
    }
]

# Demographic Factors
ages = [25, 50, 75]
genders = ["Male", "Female"]
educations = ["High School", "Bachelor's Degree", "Master's Degree"]
politics = ["Democrat", "Republican", "Independent"]
severities = ["Mild", "Moderate", "Severe"]

def get_occupation(edu):
    """Map education level to a representative occupation."""
    if edu == "High School": return "Service Worker"
    if edu == "Bachelor's Degree": return "Office Manager"
    if edu == "Master's Degree": return "Professional Consultant"
    return "Unemployed"

# Generate All Combinations
personas = []

for profile, severity, age, gender, edu, pol in itertools.product(clinical_profiles, severities, ages, genders, educations, politics):
    
    # Create a unique ID
    # Format: Code_Severity_Gender_Age_EduShort_PolShort
    edu_short = edu.split()[0] # "High", "Bachelor's", "Master's"
    pol_short = pol[:3] # "Dem", "Rep", "Ind"
    persona_id = f"{profile['code']}_{severity}_{gender}_{age}_{edu_short}_{pol_short}"
    
    persona = {
        "id": persona_id,
        "age": age,
        "gender": gender,
        "education": edu,
        "occupation": get_occupation(edu),
        "political_affiliation": pol,
        "clinical_profile": {
            "diagnosis": profile["diagnosis"],
            "severity": severity,
            "symptoms": profile["symptoms"]
        }
    }
    personas.append(persona)
