# Plan: Replicating the GenAI Engineer Study

This document outlines the steps to replicate the empirical study on the GenAI Engineer profession, based on the methodology from the paper "What Is an AI Engineer? An Empirical Analysis of Job Ads in The Netherlands" (`docs/genAI-replaced-CAIN2022.txt`).

Our mission is to understand the role, skills, and expectations for a **GenAI Engineer**.

---

## Phase 1: Scoping and Preparation

1.  **Finalize Research Questions:** We will adapt the original research questions to focus squarely on the GenAI Engineer.

    - **RQ1a:** Which job tasks are expected from GenAI engineers?
    - **RQ1b:** Are the job tasks expected from GenAI engineers more focused on model development/fine-tuning or on software engineering/integration?
    - **RQ2:** What are the most frequently mentioned tools and technologies (e.g., LLMs, frameworks, platforms) expected to be used by GenAI engineers?
    - **RQ3:** Which soft skills are required for the job of GenAI engineer?

2.  **Define "GenAI Engineer":** We must establish a clear working definition. The original paper's definition of GenAI Engineering is a starting point, but we must update it to reflect the modern landscape dominated by Large Language Models (LLMs) and other generative models.

3.  **Identify Data Source:** The original study used the Jobfeed database. We must identify and secure access to a suitable source of job ad data. This could be a commercial database or a strategy for ethically scraping public job boards like LinkedIn, Indeed, etc., where permitted.

---

## Phase 2: Data Collection and Filtering

1.  **Design the Search Query:** We need a new, precise query. We will move beyond the original `(developer || engineer) & (AI || ML || DL)`. Our new query should include terms like:

    - "GenAI Engineer"
    - "Generative AI Engineer"
    - "LLM Engineer"
    - Keywords for specific models (e.g., GPT, Claude, Llama) and frameworks (e.g., LangChain, Hugging Face).

2.  **Set Inclusion/Exclusion Criteria:**

    - **Inclusion:** Roles focused on building or integrating generative AI systems. Ads published within a recent timeframe (e.g., the last 18-24 months) to capture the post-ChatGPT hiring boom.
    - **Exclusion:** Ads with no detailed job description, roles for traditional ML/AI, pure data science/analytics roles, and non-technical/managerial positions.

3.  **Execute Search and Manual Filtering:** We will run our query to gather a large pool of ads. This will be followed by a manual review process, as performed in the original study, to select the final, relevant dataset.

---

## Phase 3: Data Analysis and Coding

1.  **Metadata Analysis:** We will first analyze the high-level metadata of our selected job ads to understand the landscape:

    - Publication dates (to see trends)
    - Industry and sector
    - Educational requirements
    - Common job titles

2.  **Automated Thematic Coding with Human Validation:** To analyze a much larger dataset with scientific rigor, we will automate the coding process using the Gemini API, validated by human experts. The analysis will use a simplified four-profile system to categorize each job ad:

    - **`AI Engineer`**: Generalist role with balanced tasks across both ML and Generative AI.
    - **`ML Engineer`**: Specialist focused on predictive modeling, MLOps, and traditional data science.
    - **`GenAI Engineer`**: Specialist focused on language models, interaction, and application development (RAG, fine-tuning).
    - **`Ambiguous / Not Relevant`**: A catch-all for ads that are non-technical, too vague, or do not fit the primary profiles.

    - **a. Develop a "Coding Book":** We will first create a comprehensive document defining every category and sub-category for job tasks, technologies, and soft skills, all aligned with the four-profile system.
    - **b. Engineer and Refine Master Prompt:** We will craft a detailed master prompt for the Gemini API based on the new, simplified Coding Book.
    - **c. Full-Scale Automated Coding:** The new, refined prompt will be used to process the entire dataset of job ads automatically. This is a complete re-analysis of the data.
    - **d. Scientific Validation (`Steekproef`):** To ensure our automated method is scientifically sound, we will perform a final validation. A human expert will manually code a new, random sample (e.g., 50-100 ads) of the AI-coded data. We will then calculate the Inter-Rater Reliability (e.g., Cohen's Kappa) between the human and AI "raters". A high score will validate our approach and allow us to report the accuracy of our automated method. This step is critical for ensuring the trustworthiness of our final results.

3.  **Synthesize Findings:** We will analyze the structured data from the validated coding phase to answer our research questions, identifying key patterns and frequencies.

---

## Phase 4: Reporting and Synthesis

1.  **Discuss Implications:** We will interpret our findings to understand their meaning for the industry, education, and the research community.

    - What profiles of GenAI Engineers exist?
    - How should universities adapt their curricula?
    - What should companies look for when hiring?

2.  **Propose a GenAI Engineering Lifecycle:** Based on the job tasks we identify, we will propose an updated lifecycle model that reflects how GenAI systems are built and maintained in practice.

3.  **Acknowledge Limitations:** We will transparently document any threats to the validity of our study (e.g., biases in our data source, geographic focus).

4.  **Draft the Paper:** We will write our own research paper, presenting our findings to the world and contributing to the understanding of this new and vital profession.
