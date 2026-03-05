"""Shared run configuration. All scripts import paths from here.

Set RUN_ID via environment variable or let it default to today's date.
  RUN_ID=2026-03-03 python src/clinical_persona_sim.py
"""

import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RUN_ID = os.environ.get("RUN_ID", datetime.now().strftime("%Y-%m-%d"))

DATA_DIR = PROJECT_ROOT / "data" / "runs" / RUN_ID
FIGURES_DIR = PROJECT_ROOT / "figures" / "runs" / RUN_ID

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Data paths
SIMULATION_RESULTS = DATA_DIR / "simulation_results.csv"
SCORED_RESULTS = DATA_DIR / "scored_results.csv"
ANALYSIS_RESULTS = DATA_DIR / "analysis_results.csv"

# Figure paths
FIGURE1_NEW_PDF = FIGURES_DIR / "figure1_new.pdf"
FIGURE1_NEW_PNG = FIGURES_DIR / "figure1_new.png"
