# GenAI/ML Engineer Job Market Analysis Pipeline

This document outlines the end-to-end data analysis pipeline, from raw, agent-analyzed job advertisements to the final generated report. It is designed to be used by either an automated coding bot or a human researcher to reproduce the analysis.

## Pipeline Overview

The pipeline is a sequence of Python scripts that progressively process, analyze, and visualize the data. Each step builds upon the artifacts created by the previous one.

**Workflow:**
`Raw JSON Analyses` -> **Consolidate** -> **Clean** -> **Descriptive Analysis & Topic Modeling** -> **Correlate & Run Stats** -> **Generate Report**

---

### Prerequisites

Before running the pipeline, ensure the following are set up:

1.  **Python Environment:** A Python 3.12 virtual environment is required. [[memory:7590819]]
2.  **Dependencies:** All required packages must be installed. This project uses `uv` for dependency management. [[memory:7590819]]
3.  **spaCy Model:** The topic modeling script requires the `en_core_web_sm` model. Install it with:
    ```bash
    source .venv/bin/activate
    python -m spacy download en_core_web_sm
    ```

---

## Step 0: Initial Job Ad Analysis (Agent-based)

This is the conceptual first step where the analysis begins.

- **Purpose:** To analyze each raw job ad (`consolidated_deduplicated.csv`) and produce a structured JSON file containing a profile classification (e.g., `GenAI Engineer`) and a thematic analysis based on the `CODING_BOOK.md`.
- **Action:** This step is performed by an external agent (e.g., a Gemini-based coding bot) or a human researcher. The goal is to process each job ad and generate a corresponding JSON file.
- **Inputs:** `data/consolidated_deduplicated.csv`
- **Outputs:** A collection of structured JSON files.
  - **Location:** `data/automated_analysis/`
  - **Format:** `analysis_job_{job_id}.json`

---

## Step 1: Consolidate All Analyses

- **Purpose:** To merge the hundreds of individual JSON analysis files into a few well-structured CSV files, making the data easier to work with in aggregate.
- **Script:** `scripts/consolidate_automated_analysis.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/consolidate_automated_analysis.py
  ```
- **Inputs:** All `analysis_job_*.json` files located in `data/automated_analysis/`.
- **Outputs:** Three CSV files.
  - `data/automated_analysis_consolidated.csv`: A "tidy" long-form dataset where each row represents a single observation (e.g., a skill, a tool, a task).
  - `data/automated_analysis_profiles.csv`: A file mapping each `job_id` to its assigned profile (`GenAI Engineer`, `ML Engineer`, etc.).
  - `data/automated_analysis_per_job.csv`: A file containing all the structured analysis data for each job, with complex data stored as JSON strings.

---

## Step 2: Clean Analysis Output

- **Purpose:** To clean and standardize the consolidated data. This crucial step removes inconsistencies (e.g., stray backticks, category prefixes like `TASK1:`) that would otherwise skew the analysis.
- **Script:** `scripts/clean_analysis_output.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/clean_analysis_output.py
  ```
- **Inputs:** `data/automated_analysis_consolidated.csv` and `data/automated_analysis_profiles.csv`.
- **Outputs:** The script overwrites the input files with their cleaned versions.
  - `data/automated_analysis_consolidated.csv` (cleaned)
  - `data/automated_analysis_profiles.csv` (cleaned)

---

## Step 3: Descriptive Analysis

- **Purpose:** To generate high-level descriptive statistics and visualizations of the cleaned data. This provides the first overview of the job market landscape.
- **Script:** `scripts/descriptive_analysis.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/descriptive_analysis.py
  ```
- **Inputs:** The two cleaned CSV files from the previous step.
- **Outputs:** A series of PNG charts and summary CSVs.
  - **Location:** `data/analysis_results/`
  - **Artifacts:**
    - `profile_distribution.png`: Bar chart of job profile counts.
    - `job_task_distribution.png`: Bar chart of job task frequencies.
    - `technology_distribution.png`: Bar chart of technology category frequencies.
    - `top_tools_overall.csv`: CSV listing the most common technologies.
    - ...and several other charts and summary tables.

---

## Step 4: Topic Modeling

- **Purpose:** To perform an exploratory analysis of the raw job description text, uncovering hidden thematic structures (topics) that exist in the data beyond our predefined categories.
- **Script:** `scripts/topic_modeling.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/topic_modeling.py
  ```
- **Inputs:** `data/consolidated_deduplicated.csv` (the original raw job data).
- **Outputs:**
  - **Location:** `data/analysis_results/`
  - **Artifacts:**
    - `topic_definitions.csv`: The top keywords that define each discovered topic.
    - `job_topic_mapping.csv`: A mapping of each `job_id` to its most dominant topic.
    - `topic_modeling_results.txt`: A human-readable summary of the topics.

---

## Step 5: Correlate Topics with Profiles

- **Purpose:** To synthesize the results of the main analysis (profiles) with the exploratory analysis (topics). This step reveals which underlying themes are most prominent for each job profile.
- **Script:** `scripts/analyze_topics_by_profile.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/analyze_topics_by_profile.py
  ```
- **Inputs:** `data/automated_analysis_profiles.csv`, `data/analysis_results/job_topic_mapping.csv`, and `data/analysis_results/topic_definitions.csv`.
- **Outputs:**
  - **Location:** `data/analysis_results/`
  - **Artifacts:**
    - `crosstab_profiles_vs_topics.csv`: A table showing the raw counts of topic distribution per profile.
    - `heatmap_profiles_vs_topics.png`: A heatmap visualizing the percentage distribution of topics within each profile.

---

## Step 6: Statistical Analysis

- **Purpose:** To add statistical rigor to our findings by performing formal significance tests and deeper analyses like technology co-occurrence.
- **Script:** `scripts/statistical_analysis.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/statistical_analysis.py
  ```
- **Inputs:** The cleaned consolidated and profiles CSV files.
- **Outputs:** A collection of statistical results and visualizations.
  - **Location:** `data/analysis_results/`
  - **Artifacts:**
    - `chi_squared_results.csv`: Results of the Chi-Squared tests, showing if differences between profiles are statistically significant.
    - `technology_cooccurrence_heatmap.png`: A heatmap showing which technologies are frequently mentioned together.
    - `normalized_crosstab_*.csv`: Tables showing the percentage-based distribution of skills/tasks/techs within each profile, making comparison easier.
    - `topic_profile_correlation.md`: A markdown table summarizing the topic/profile correlation.

---

## Step 7: Generate Final Report

- **Purpose:** To assemble all the generated artifacts—charts, tables, and statistical summaries—into a single, comprehensive, and human-readable markdown report.
- **Script:** `scripts/generate_report.py`
- **Action:**
  ```bash
  source .venv/bin/activate
  python scripts/generate_report.py
  ```
- **Inputs:** All the PNG, CSV, and MD artifacts created in the previous steps, located in `data/analysis_results/`.
- **Outputs:** The final report file.
  - **Artifact:** `REPORT.md`
  - **Location:** Project root directory.
