# LLM Clinical Persona Simulation

**The threat of synthetic respondents extends to clinical mental health screening**

Kianté Fernandez (1), Laura A. Berner (2), Blair R. K. Shevlin (2)

1. Department of Psychology, University of California, Los Angeles, Los Angeles, California
2. Center for Computational Psychiatry, Department of Psychiatry, Icahn School of Medicine at Mount Sinai, New York, New York

This repository contains the simulation code, data, and manuscript for a study evaluating whether a commercially available large language model can generate clinically plausible responses on validated psychiatric screening instruments. Synthetic personas with assigned diagnoses, demographics, and severity levels complete standardized assessments via Google Gemini 2.0 Flash.

## Repository Structure

```
LLM-clinical/
├── src/                    Source code
│   ├── run_config.py           Run ID and path configuration
│   ├── personas.py             Synthetic persona generation
│   ├── batteries.py            Clinical instrument definitions
│   ├── clinical_persona_sim.py Main simulation engine (Gemini API)
│   ├── score_results.py        Response scoring
│   ├── plot_figure1_new.R      Clinical target groups figure
│   ├── run_analyses.R          Statistical analyses
│   └── list_models.py          Utility: list Gemini models
├── data/
│   ├── runs/{RUN_ID}/          Per-run outputs (date-stamped)
│   │   ├── simulation_results.csv
│   │   ├── scored_results.csv
│   │   ├── descriptive_results.csv
│   │   └── analysis_results.csv
│   ├── simulation_results.csv
│   └── scored_results.csv
├── figures/
│   └── runs/{RUN_ID}/          Per-run figures (date-stamped)
├── paper/jama_submit/      Manuscript
├── .env.example
├── requirements.txt
└── README.md
```

## Data Pipeline

```
src/personas.py            Define 2106 synthetic clinical personas
       |
src/batteries.py           Define 7 clinical assessment instruments
       |
src/clinical_persona_sim.py    Run personas through instruments via Gemini API
       |                       -> data/runs/{RUN_ID}/simulation_results.csv
src/score_results.py       Score raw responses using standard rubrics
       |                   -> data/runs/{RUN_ID}/scored_results.csv
src/plot_figure1_new.R     Clinical target groups figure
       |                   -> figures/runs/{RUN_ID}/
src/run_analyses.R         Statistical analyses
                           -> data/runs/{RUN_ID}/ + figures/runs/{RUN_ID}/
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

All Python scripts should be run from the `src/` directory. R scripts from the project root.

Each run is date-stamped automatically (defaults to today). Override with `RUN_ID` env var.

### Run the full pipeline

```bash
cd src

# 1. Simulate (requires GOOGLE_API_KEY in .env)
python clinical_persona_sim.py

# 2. Score
python score_results.py

# 3. Plot + analyze (R, run from project root)
cd ..
Rscript src/plot_figure1_new.R
Rscript src/run_analyses.R
```

### Test with mock responses (no API calls)

```bash
cd src
python clinical_persona_sim.py --mock

```
