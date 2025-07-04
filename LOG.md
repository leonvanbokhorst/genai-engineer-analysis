# Project Log

This document tracks the key decisions and steps taken during the GenAI Engineer analysis project.

## 2024-07-26: Data Deduplication

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
