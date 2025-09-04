# GenAI Engineer Job Market Analysis

This project provides a flexible, automated pipeline to analyze job market data for AI-related engineering roles, inspired by the methodology in the paper "What Is an AI Engineer?" (Heck et al., CAIN 2022). This implementation replays and extends the paper's analysis with a new dataset, focusing on the **Generative AI Engineer** and **ML Engineer** roles.

The full methodology, findings, and plots can be found in the auto-generated **[REPORT.md](REPORT.md)**.

## Research & Documentation

The `/docs` directory contains the foundational research for this project:

- **[CAIN2022.pdf](docs/CAIN2022.pdf)**: The original paper by Heck et al. that inspired the five-category analysis framework (Business Understanding, Data Engineering, Modeling, Software Development, Operations).
- **[The AI Job Market for Engineers in 2025](docs/The%20AI%20Job%20Market%20for%20Engineers%20in%202025_%20A%20Comprehensive%20Field%20Research%20Report.md)**: A comprehensive manuscript detailing the findings from this project's analysis of the AI job market.
- **[/docs/AI Terminology Evolution](docs/AI%20Terminology%20Evolution/The%20Evolving%20Definition%20of%20AI:%20A%20Historical%20and%20Contemporary%20Analysis.md)**: A series of research manuscripts analyzing the historical and contemporary definitions of "Artificial Intelligence" and related terms, providing crucial context for the classification schema used in this project.

---

## How to Use the Pipeline

This pipeline is designed to be fully automated. After setup, running the scripts in order will reproduce the analysis from raw data to the final report.

### 1. Prerequisites

- Python 3.12+
- `uv` (a fast Python package installer and resolver)

### 2. Setup

**a. Create and Activate a Virtual Environment:**

```bash
uv venv -p python3.12
source .venv/bin/activate
```

**b. Install Dependencies:**

```bash
uv sync
```

### 3. Running the Full Pipeline

**a. Consolidate Raw Data:**
Place your source `.xls` files into the `/data/raw` directory, then run:

```bash
# Consolidate XLS files
python scripts/consolidate_data.py

# Deduplicate records
python scripts/deduplicate_data.py
```

**b. Run Automated Analysis:**
This script uses the Gemini API to analyze each job ad based on the `CODING_BOOK.md` schema.

```bash
python scripts/analysis_pipeline.py
```

**c. Consolidate JSON Results:**
This script flattens the individual JSON analysis files into tidy CSVs for analysis.

```bash
python scripts/consolidate_automated_analysis.py
```

**d. Generate Descriptive Analysis & Plots:**
This script computes all the CAIN-style metrics, cross-tabulations, and generates the plots.

```bash
python scripts/descriptive_analysis.py
```

**e. Generate the Final Report:**
This script assembles the plots and tables into a final `REPORT.md` file.

```bash
python scripts/generate_report.py
```
