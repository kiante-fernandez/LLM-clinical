# LLM Clinical Persona Simulation

Evaluates how large language models simulate clinical patient responses across validated psychiatric instruments. Synthetic personas with assigned diagnoses, demographics, and severity levels complete standardized assessments via Google Gemini, allowing analysis of LLM diagnostic fidelity.

Based on Westwood (2025), adapted for clinical follow-up studies.

## Study Design

- **13 diagnoses**: MDD, Bipolar I, GAD, PTSD, OCD, Schizophrenia, Prodromal Syndrome, Alzheimer's, Parkinson's Dementia, Frontotemporal Dementia, Anorexia Nervosa, Bulimia Nervosa, Binge Eating Disorder
- **Demographics**: 3 ages (25/50/75) x 2 genders x 3 education levels x 3 political affiliations x 3 severity levels
- **2,028 unique personas**, each completing all 7 batteries
- **7 clinical instruments**: PHQ-9, GAD-7, OCI-R, PCL-5, MDQ, PQ-16, EDE-Q

## Repository Structure

```
LLM-clinical/
├── src/                    Source code
│   ├── personas.py             Synthetic persona generation
│   ├── batteries.py            Clinical instrument definitions
│   ├── clinical_persona_sim.py Main simulation engine (Gemini API)
│   ├── score_results.py        Response scoring
│   ├── plot_results.py         Publication-ready boxplots
│   ├── plot_edeq_specific.py   EDE-Q item-level analysis
│   └── list_models.py          Utility: list Gemini models
├── data/                   Simulation outputs
│   ├── simulation_results.csv  Raw responses (233K rows)
│   └── scored_results.csv      Scored battery totals
├── figures/                Generated plots
│   ├── publication_ready_plot_v5.png
│   └── edeq_specific_plot.png
├── paper/                  Manuscript (Nature Medicine Brief Communication)
│   ├── main.tex
│   ├── references.bib
│   └── figures/
│       └── figure1.png
├── .env.example
├── requirements.txt
└── README.md
```

## Data Pipeline

```
src/personas.py            Define 2,028 synthetic clinical personas
       |
src/batteries.py           Define 7 clinical assessment instruments
       |
src/clinical_persona_sim.py    Run personas through batteries via Gemini API
       |                       -> data/simulation_results.csv
src/score_results.py       Score raw responses using standard rubrics
       |                   -> data/scored_results.csv
src/plot_results.py        Generate publication-ready boxplots
       |                   -> figures/publication_ready_plot_v5.png
src/plot_edeq_specific.py  EDE-Q item-level analysis
                           -> figures/edeq_specific_plot.png
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file (see `.env.example`):
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

## Usage

All scripts should be run from the `src/` directory:

```bash
cd src
```

Run the full simulation (requires API key):
```bash
python clinical_persona_sim.py
```

Test with mock responses (no API calls):
```bash
python clinical_persona_sim.py --mock
```

Score the results:
```bash
python score_results.py
```

Generate plots:
```bash
python plot_results.py
python plot_edeq_specific.py
```
