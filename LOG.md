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
