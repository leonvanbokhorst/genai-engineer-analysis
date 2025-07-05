import pandas as pd
from pathlib import Path

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_RESULTS_PATH = WORKSPACE_DIR / "data" / "analysis_results.csv"
ORIGINAL_DATA_PATH = WORKSPACE_DIR / "data" / "consolidated_deduplicated.csv"
OUTPUT_PATH = WORKSPACE_DIR / "data" / "validation_sample.csv"
SAMPLE_SIZE = 50


def main():
    """
    Creates a random sample of N records from the analysis results for manual validation.
    """
    print("--- Creating Validation Sample ---")

    # 1. Load the consolidated analysis results
    try:
        df_analysis = pd.read_csv(ANALYSIS_RESULTS_PATH)
        print(f"Loaded {len(df_analysis)} records from {ANALYSIS_RESULTS_PATH}")
    except FileNotFoundError:
        print(f"ERROR: Analysis results file not found at {ANALYSIS_RESULTS_PATH}")
        return

    # 2. Load the original, deduplicated data to get the job ad text
    try:
        df_original = pd.read_csv(ORIGINAL_DATA_PATH)
        # Create 'full_text' and 'job_id' to match the analysis file
        df_original["full_text"] = (
            df_original["Vacaturetitel"].fillna("")
            + "\n\n"
            + df_original["Functieomschrijving"].fillna("")
        )
        df_original["job_id"] = df_original.index
        print(f"Loaded {len(df_original)} records from {ORIGINAL_DATA_PATH}")
    except FileNotFoundError:
        print(f"ERROR: Original data file not found at {ORIGINAL_DATA_PATH}")
        return

    # 3. Take a random sample
    if len(df_analysis) < SAMPLE_SIZE:
        print(
            f"Warning: The number of records ({len(df_analysis)}) is less than the desired sample size ({SAMPLE_SIZE}). Using all records."
        )
        sample_df = df_analysis
    else:
        sample_df = df_analysis.sample(
            n=SAMPLE_SIZE, random_state=42
        )  # Using a random_state for reproducibility

    print(f"Randomly selected {len(sample_df)} records for validation.")

    # 4. Merge with original data to get the full job ad text
    # We select only the necessary columns from the original data to merge
    df_merged = pd.merge(
        sample_df,
        df_original[["job_id", "Vacaturetitel", "full_text"]],
        on="job_id",
        how="left",
    )

    # 5. Add columns for manual validation input
    df_merged["validator_profile"] = ""
    df_merged["validator_confidence"] = ""
    df_merged["validator_notes"] = ""

    print("Added columns for manual validation input.")

    # 6. Reorder columns for convenience
    final_columns = [
        "job_id",
        "Vacaturetitel",
        "assigned_profile",  # AI's conclusion
        "validator_profile",  # Human's conclusion
        "confidence_score",  # AI's confidence
        "validator_confidence",  # Human's confidence
        "profile_rationale",  # AI's reasoning
        "validator_notes",  # Human's notes
        "full_text",
        "job_tasks",
        "technologies",
        "soft_skills",
    ]
    df_final = df_merged[final_columns]

    # 7. Save the sample to a new CSV
    df_final.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"\n--- Validation Sample Created ---")
    print(f"File saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
