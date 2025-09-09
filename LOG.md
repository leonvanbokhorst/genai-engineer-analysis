# Project Log

This document tracks the key decisions and steps taken during the GenAI Engineer analysis project.

## 2025-07-04: Data Deduplication

The initial dataset, `data/consolidated.csv`, required cleaning to remove duplicate entries. The process was iterative to ensure accuracy.

### Step 1: Initial Deduplication Attempt

- **Action:** A script (`scripts/deduplicate_data.py`) was created to remove duplicates.
- **Criteria:** The first attempt used only the `Vacaturelink (origineel)` column to identify unique records.
- **Result:** This reduced the dataset from 1283 to 147 rows, removing 1136 records.
- **Conclusion:** This was deemed far too aggressive, as it likely removed non-duplicate jobs that were posted without a unique URL.

### Step 2: Refining Deduplication Criteria

- **Action:** The script was updated to use a combination of columns.
- **Criteria:** `Organisatienaam`, `Vacaturetitel`, `Standplaats`, and `Vacaturelink (origineel)`.
- **Result:** This reduced the dataset from 1283 to 1210 rows, removing 73 duplicates.
- **Conclusion:** This was a significant improvement and a more reasonable result.

### Step 3: Final, Comprehensive Deduplication

- **Action:** To be absolutely certain, more columns were added to the check.
- **Criteria:** `Organisatienaam`, `Vacaturetitel`, `Standplaats`, `Vacaturelink (origineel)`, `Beroepsgroep`, `Beroepsklasse`, `Beroep`, `Jaar (van datum gevonden)`, and `Maand (van datum gevonden)`.
- **Result:** This final pass reduced the dataset from 1283 to 1272 rows, removing 11 duplicates that the previous step missed.
- **Conclusion:** This is the final, clean dataset.

The resulting deduplicated data is stored in `data/consolidated_deduplicated.csv`.

---

## 2025-07-04: Evolving the Research Methodology

During the initial phase of the manual coding pilot study, a key methodological challenge was identified, prompting an evolution of our analytical approach.

### The Challenge: Classifying AI-Adjacent Roles

While coding the first few job ads (specifically `#33 Senior Flutter Engineer`), we encountered a role that was fundamentally a software engineering position but was explicitly designed to _interact with_ or _consume services from_ a Generative AI platform.

A simple binary classification (i.e., is this a "GenAI Engineer" or not?) proved insufficient.

- **Excluding the role** would mean losing valuable data about a significant portion of the GenAI job ecosystem.
- **Including it without distinction** would dilute the definition of a "Core GenAI Engineer" and muddy the analysis.

### The Solution: Introducing GenAI Engineer Profiles

To address this, we made the decision to move beyond a single label and introduce a more nuanced, three-tiered classification system for the roles we analyze:

1.  **Core GenAI Engineer:** A role with a balanced mix of tasks from both `Core Software Engineering` and `GenAI Specialization` categories.
2.  **AI-Adjacent Software Engineer:** A role that is primarily a software engineering position but explicitly integrates with or consumes GenAI services.
3.  **GenAI Specialist:** A role heavily focused on `GenAI Specialization` tasks (modeling, data, prompt engineering) with fewer software integration responsibilities.

### Rationale and Justification

This evolution is an **extension, not a replacement,** of the original paper's methodology. We are still performing the same detailed coding of tasks, tools, and skills. However, this profiling layer allows us to:

- Capture the full spectrum of roles in the GenAI landscape.
- Provide a much richer and more accurate analysis of what companies are actually hiring for.
- Directly test the "software engineering first" hypothesis by quantifying the prevalence of each profile.

This decision will be applied to all ads coded during the pilot study and the subsequent automated analysis.

---

## 2025-07-05: Refining Analysis Profiles and Process

Upon reviewing the initial automated analysis approach, a critical need for further refinement was identified to handle edge cases and ensure the scientific rigor of our results.

### The Challenge: Ambiguity of "AI-Adjacent" and Irrelevant Ads

1.  **"AI-Adjacent" was too broad:** The definition could inadvertently include software engineers who merely _use_ AI-assisted tools (e.g., GitHub Copilot) rather than building software that _integrates_ AI as a feature.
2.  **Lack of a "Not Relevant" category:** The initial keyword-based data collection inevitably pulled in some job ads that, upon closer inspection, were completely unrelated to either software or AI engineering (e.g., sales roles mentioning "AI").

### The Solution: Stricter Definitions and a Validation Phase

Following a discussion inspired by Petra's feedback, the following actions were taken:

1.  **Refined `AI-Adjacent` Definition:** The `CODING_BOOK.md` and `master_prompt.md` were updated to clarify that this profile is for roles where the _output_ of the work is an AI-powered feature, not just roles using AI tools for productivity.
2.  **Added `Not Relevant` Profile:** A new profile, `Not Relevant`, was introduced to formally categorize and exclude job ads that do not fit our study's criteria. This aligns with the implicit filtering methodology of the original CAIN2022 paper.
3.  **Adopted Post-Analysis Validation:** A new step was formally added to our `PLAN.md`. After the automated analysis is complete, a random sample of the results will be manually reviewed. This will allow us to validate the accuracy of the automated system and quantify its performance on ambiguous or edge-case job ads.
4.  **Cleared Obsolete Results:** All analysis files generated with the old, less precise methodology were deleted from `data/automated_analysis/` to ensure a clean slate for the upcoming, more rigorous analysis run.

---

## 2025-07-05 (PM): Final Profile Refinement

A final, crucial distinction was proposed to ensure the highest fidelity in our analysis.

### The Challenge: Differentiating AI Builders from AI Users

The refined definition of `AI-Adjacent Software Engineer` was good, but it didn't fully separate a key group: standard Software Engineers who work in an "AI-first" company or use AI-assisted tools (like Copilot) for productivity, but whose work product is not itself an AI-powered system.

### The Solution: A Five-Profile System

A new profile was created to capture this distinction:

1.  **`Software Engineer` Profile Added:** This new profile is for roles that are purely `Core Software Engineering` (Macro-Category A). They do not build or integrate AI models into the product. This distinguishes them from `AI-Adjacent` roles, which _do_ integrate AI into the product.
2.  **Five-Profile Model:** Our final classification system now consists of five distinct profiles: `Core GenAI Engineer`, `AI-Adjacent Software Engineer`, `Software Engineer`, `GenAI Specialist`, and `Not Relevant`.
3.  **Documentation Updated:** The `CODING_BOOK.md` and `master_prompt.md` were both updated to reflect this final, more nuanced system before commencing the definitive analysis run.

---

## 2025-07-05 (Evening): Adding Confidence Scoring

To better handle ambiguity and assess the reliability of the automated analysis on a per-job basis, a confidence scoring mechanism was introduced.

### The Challenge: Quantifying Uncertainty

Some job ads are vague, contradictory, or lack detail. A simple classification doesn't capture the model's potential uncertainty in these cases.

### The Solution: Self-Reflection in the Prompt

Instead of a more complex ensemble method, a "self-reflection" step was added directly into the `master_prompt.md`:

1.  **Confidence Score:** The prompt now instructs the model to add a `confidence` block to its JSON output, containing a `score` (1-5) and a `reasoning` field.
2.  **Explicit Instruction:** The model must assess its own confidence based on the clarity and consistency of the job ad it just analyzed.
3.  **Benefit:** This provides a direct, per-item measure of confidence without increasing analysis time or cost, allowing us to easily identify and review low-confidence classifications later.

---

## 2025-07-05 (Final Refinement): Distinguishing ML vs. GenAI Roles

The last and most subtle refinement was to differentiate between traditional Machine Learning engineering and modern Generative AI engineering.

### The Challenge: The "AI Engineer" Title is Ambiguous

The term "AI Engineer" is often used to describe both classical ML roles (focused on predictive models, MLOps) and the newer GenAI roles (focused on LLMs). Grouping them together as `Core GenAI Engineer` would obscure a key trend in the job market.

### The Solution: A Six-Profile System with Clear Specializations

The classification system was expanded to its final six-profile form:

1.  **`Core GenAI Engineer` vs. `Core ML Engineer`:** The core engineering profile was split to distinguish between those working with generative tech versus traditional ML.
2.  **`GenAI Specialist` vs. `ML Specialist`:** The specialist profile was also split to maintain symmetry, clearly identifying roles focused purely on traditional data science.
3.  **Final System:** The definitive list of profiles is now: `Core GenAI Engineer`, `Core ML Engineer`, `AI-Adjacent Software Engineer`, `Software Engineer`, `GenAI Specialist`, `ML Specialist (Data Scientist)`, and `Not Relevant`. All documentation was updated to reflect this.

---

## 2025-07-08: Definitive Analysis and Consolidation

The full, definitive automated analysis and subsequent consolidation of the results are complete.

### Actions

1.  **Corrected Analysis Run:** The `scripts/analyze_job_ad.py` script was corrected to use the deduplicated dataset (`data/consolidated_deduplicated.csv`) and was executed to analyze all 1272 job ads. The results were saved to a new directory, `data/automated_analysis_deduplicated/`, to preserve the original run.
2.  **Consolidated Results:** The `scripts/consolidate_analysis.py` script was run to merge the individual JSON outputs into a single master file.
    - During this process, 49 files with API response errors (e.g., malformed JSON, empty responses) were automatically identified and excluded.
    - The remaining 1223 clean records were consolidated.

### Outcome

- A single, unified dataset, `data/analysis_results.csv`, has been created, containing the structured analysis for 1223 job advertisements.
- This file is now the primary source for the subsequent validation, analysis, and visualization phases of the project.

---

## 2025-07-05: Initial Validation and Methodological Pivot

Following the successful analysis run, a new phase of the project began: manual validation of the AI's classifications.

### Actions

1.  **Validation Sample Creation:** A random sample of 50 job ads was created (`data/validation_sample.csv`) from the 1,223 analyzed records.
2.  **Interactive Validation Tool:** To facilitate an efficient and accurate review, an interactive web application was built using Streamlit (`scripts/validation_app.py`). This tool presents the AI's analysis side-by-side with the original job ad text.
3.  **Initial Human-in-the-Loop Validation:** The Jedi Master (Lonn) began the validation process using the Streamlit tool.

### Key Finding and Decision

- **Insight:** After reviewing approximately 10 records, a critical insight was uncovered. The current six-profile classification system (`Core GenAI Engineer`, `Core ML Engineer`, etc.) is **too granular**. The subtle distinctions between the profiles, while logical in theory, proved difficult for the model to apply consistently to real-world, often ambiguous, job descriptions.
- **Decision:** To improve the robustness and clarity of our findings, a decision was made to simplify the classification schema. The next step will be to revise the `CODING_BOOK.md` to reflect broader, more distinct categories before proceeding further with the validation or final analysis.

---

## 2025-07-05 (PM): The Final Simplification

Based on the insight from the initial validation, a final, decisive pivot was made to the classification schema to maximize clarity and analytical power.

### Action: Schema Collapse

The previous, multi-layered profile system was collapsed into four, high-level archetypes:

1.  **`AI Engineer`**: A generalist role with significant, balanced tasks across both Machine Learning and Generative AI.
2.  **`ML Engineer`**: A specialist role focused on predictive modeling, MLOps, and traditional data science tasks.
3.  **`GenAI Engineer`**: A specialist role focused on language models, interaction, and application development (e.g., RAG, fine-tuning).
4.  **`Ambiguous / Not Relevant`**: A catch-all category for any job ad that does not clearly fit one of the three primary profiles, is non-technical, or is too vague to classify.

### Consequence: Analysis Reset

- **Obsolete Results Archived:** This new schema renders all previous analysis obsolete. Per the Master's instruction, all 1,223 analysis files and the corresponding summary CSV have been moved to a `data_archive/` directory for historical reference.
- **Full Re-Analysis Required:** The project will now proceed with updating the core `CODING_BOOK.md` and `master_prompt.md` before re-running the entire automated analysis pipeline from the beginning. This ensures the final results are based on a consistent, robust, and simplified methodology.

---

## 2025-07-05: The Definitive Analysis Pipeline

Following the decision to simplify the classification schema, a new, definitive analysis pipeline was constructed, incorporating all lessons learned from previous iterations.

### Actions & Methodological Improvements

1.  **Definitive `CODING_BOOK.md` Created:** A new coding book (`v3 - Definitive`) was created. It combines the simplified 4-profile classification with a detailed, evidence-based thematic analysis, directly inspired by the five core job task categories in the CAIN 2022 paper (`TASK1: Business Understanding`, `TASK2: Data Engineering`, etc.). This provides high-level clarity and deep, granular evidence.
2.  **Dynamic Prompting Implemented:** A new analysis script (`scripts/analysis_pipeline.py`) was built from the ground up. It dynamically constructs its prompt by reading the `CODING_BOOK.md` at runtime, ensuring it always uses the latest definitions. This replaces the old, static `master_prompt.md`, which has been deleted.
3.  **Justification Added to Prompt:** Per the Master's instruction, the prompt was further refined to require the AI analyst to provide a `justification` for every `job_task` it identifies, adding a crucial layer of transparency to the results.
4.  **Enriched Consolidation Script:** A new consolidation script (`scripts/consolidate_results.py`) was created. It will produce a "tidy" dataset by merging the JSON analysis results with the original job data (`consolidated_deduplicated.csv`) and the full category descriptions from the `CODING_BOOK.md`, creating a single, rich file for final analysis.

### Current Status

- The definitive analysis pipeline is currently running in the background, processing all 1,272 job advertisements with the final, robust methodology.
- The project is on hold, awaiting the completion of this final analysis run.

---

## 2025-09-04: Full-Cycle CAIN-Style Analysis Pipeline

This entry marks the completion of the end-to-end analysis pipeline, from raw data processing to a final, comprehensive report, mirroring the methodology of the CAIN2022 paper.

### Actions & Methodological Improvements

1.  **CAIN-Style Consolidation:** A new script (`scripts/consolidate_automated_analysis.py`) was implemented to flatten raw JSON analyses into multiple tidy CSVs, separating profiles from categorical data to prevent duplication.
2.  **Enhanced Descriptive Analysis:** The `scripts/descriptive_analysis.py` script was significantly upgraded to:
    - Generate distribution plots for profiles, job tasks, technologies, and soft skills.
    - Implement **tool-name normalization** (e.g., "aws" -> "AWS") for accurate frequency counts.
    - Compute and save **top-N tool tables** overall and per-profile (`top_tools_*.csv`).
    - Derive and plot a **job focus** metric (RQ1b: Modeling vs. Software vs. Mixed) per job.
    - Calculate **per-job task coverage** to clarify the distinction between phrase counts and job counts.
3.  **Automated Report Generation:** A new script (`scripts/generate_report.py`) was created to automatically assemble all generated plots and key data tables into a single, comprehensive `REPORT.md` file.
4.  **Documentation Overhaul:** The project `README.md` was completely rewritten to provide clear, step-by-step instructions for running the full pipeline and to include references to the key research documents in the `/docs` directory.

### Current Status

- The project is now considered **full-cycle complete**. The pipeline can be run from start to finish to reproduce the entire analysis.
- The final outputs, including the summary `REPORT.md`, are located in `data/analysis_results/`.

---

## 2025-09-04 (PM): Exploratory Topic Modeling

To discover hidden thematic structures beyond the predefined `CODING_BOOK.md` schema, an exploratory analysis using Topic Modeling (LDA) was performed.

### Actions & Process

1.  **Data Reconstruction:** It was discovered that the raw, consolidated text file was missing. A new script (`scripts/consolidate_raw_data.py`) was created and run to rebuild the `consolidated.csv` and `consolidated_deduplicated.csv` files from the original `.xls` sources.
2.  **Topic Modeling Script:** A new script (`scripts/topic_modeling.py`) was created to preprocess the raw job descriptions and apply Latent Dirichlet Allocation (LDA) to identify 10 distinct topics.
3.  **Correlation Analysis:** The `statistical_analysis.py` script was enhanced to correlate the dominant topic of each job ad with its previously assigned profile (`GenAI Engineer`, `ML Engineer`, `Ambiguous / Not Relevant`).

### Key Findings

- The analysis successfully identified distinct thematic clusters, including topics related to core engineering, seniority, business process automation, and HR/benefits.
- Crucially, the analysis served as a powerful validation of the primary classification schema. Topics composed of generic business terms or HR-related keywords showed a very strong correlation with the `Ambiguous / Not Relevant` profile, confirming that our pipeline correctly identifies and separates these ads from true technical roles.
- The results, including the topic-profile correlation table, were added to the main `REPORT.md`.

---

## 2025-09-09: Final Analysis and Reporting Cycle

This entry documents the final, iterative cycle of the project, which involved consolidating a new batch of agent-based analyses and performing a full suite of cleaning, statistical analysis, and reporting.

### Actions & Process

1.  **Consolidation and Cleaning:** A new set of `analysis_job_*.json` files were consolidated. During this process, it was discovered that the JSON schema had evolved, and the analysis scripts were not robust enough to handle the different formats.
    - The `consolidate_automated_analysis.py` script was refactored multiple times to handle at least three different JSON structures gracefully.
    - A new, more robust data cleaning script (`scripts/clean_analysis_output.py`) was created to standardize `category_name` and `profile` fields across all consolidated files, and the old cleaning script was deleted.
2.  **Analysis and Refinement:** The full suite of analysis scripts were run:
    - `descriptive_analysis.py`: Generated initial charts.
    - `topic_modeling.py`: Performed exploratory topic analysis.
    - `analyze_topics_by_profile.py`: Correlated topics with profiles and generated a heatmap.
    - `statistical_analysis.py`: Performed Chi-Squared tests and technology co-occurrence analysis.
3.  **Heatmap Correction:** It was identified that the technology co-occurrence heatmap was cluttered with high-level category names instead of specific tools. The `statistical_analysis.py` script was refined to filter these out, producing a much cleaner and more accurate visualization.
4.  **Final Report Generation:** The `generate_report.py` script was run to assemble all the final, cleaned artifacts into the `REPORT.md`.
5.  **Comparative Analysis:** A `COMPARISON_OF_REPORTS.md` was created to document the significant improvements in the results between the pre-cleaning and post-cleaning analysis runs.
6.  **Pipeline Documentation:** A comprehensive `PIPELINE.md` was created, detailing every step of the workflow to ensure full reproducibility.
7.  **Git Hygiene:** A stray `.DS_Store` file was discovered in the repository, removed from the Git history, and added to the `.gitignore` file.

### Current Status

- The project is complete. The data pipeline is robust, the analyses are clean, and the final report and all documentation have been generated.
