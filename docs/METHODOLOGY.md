# Research Methodology

This document outlines the systematic methodology employed in the "AI Job Market for Engineers in 2025" field research report. The pipeline is designed as a multi-stage process that combines automated data extraction with rigorous manual validation to ensure the scientific validity of the findings.

## 1. Data Sourcing and Preparation

The initial phase focuses on creating a comprehensive and clean dataset of relevant job advertisements.

### 1.1. Data Consolidation

- **Source:** Raw data is extracted from the Textkernel job vacancy database, provided in multiple `.xls` files.
- **Process:** A script (`scripts/consolidate_raw_data.py`) reads these files, standardizes column names, and combines them into a single CSV file (`data/consolidated.csv`). This serves as the foundational dataset for all subsequent steps.

### 1.2. Deduplication

- **Objective:** To ensure each job vacancy is represented only once in the dataset.
- **Process:** A deduplication script (`scripts/deduplicate_data.py`) is executed. It identifies and removes duplicate entries based on a combination of key fields, such as job title, company name, and the full text of the job description. The result is a clean, deduplicated dataset (`data/consolidated_deduplicated.csv`).

## 2. Automated Analysis using AI Agent

The core of the data processing is handled by an AI agent designed to analyze the content of each job description.

- **Process:** The `scripts/analyze_job_ads_agent.py` script iterates through each job ad in the deduplicated dataset. For each ad, it invokes a Large Language Model (LLM) with a specific set of instructions.
- **Outputs:** The agent performs two main tasks:
  1.  **Profile Classification:** It categorizes the job into one of the predefined engineer profiles (e.g., ML Engineer, GenAI Engineer, AI Engineer) and provides a detailed rationale for its decision.
  2.  **Thematic Analysis:** It extracts key information related to the role, including specific **job tasks**, required **technologies**, and necessary **soft skills**. For each extracted item, the agent provides a justification and the original quote from the text.
- **Storage:** The output for each job ad is stored as a separate JSON file in the `data/automated_analysis/` directory. This granular storage prevents data loss in case of interruptions and allows for parallel processing.

## 3. Manual Validation and Review

This phase is a critical human-in-the-loop step designed to validate the accuracy and scientific rigor of the automated analysis. It addresses potential threats to validity, such as model bias or misinterpretation.

- **Tool:** A custom-built Streamlit application (`scripts/research_review_app.py`) provides a user-friendly interface for manual review.
- **Process:**
  1.  **Sampling:** A reviewer provides their name and can draw a random sample of a specified size from the entire pool of automated analyses.
  2.  **Wizard Interface:** The reviewer is presented with one job at a time in a focused, side-by-side layout. The full, original job text is always visible on the left, while the agent's analysis is presented on the right.
  3.  **Review and Decision:** The reviewer examines the agent's profile classification (and its rationale) and the thematic analysis. They then make a decision:
      - **`Accept`**: If the agent's analysis is deemed accurate and valid.
      - **`Reject`**: If the analysis is flawed. A rejection is only possible if the reviewer provides a written reason, ensuring a clear record of any identified issues.
  4.  **Data Storage:** Each decision is stored in a log file (`data/analysis_review_log.csv`), uniquely timestamped and tied to both the `job_id` and the `reviewer`. This allows for multiple independent reviews of the same job ad and preserves a full audit trail.

## 4. Final Analysis and Reporting

Once the manual validation process is complete, the verified data is used to generate the final insights for the report.

- **Process:** A series of analysis scripts (`descriptive_analysis.py`, `statistical_analysis.py`, `topic_modeling.py`) are run on the consolidated and validated data.
- **Outputs:** These scripts generate the quantitative results, visualizations (e.g., heatmaps, distributions), and statistical findings that form the basis of the research report.



