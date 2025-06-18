import pandas as pd
import os
import config  # Import our new configuration file


def load_data(file_path):
    """Loads the consolidated data from the CSV file."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
    return df


def inspect_data(df):
    """Prints a summary of the dataframe."""
    if df is not None:
        print("\n--- Data Inspection ---")
        print(f"Total jobs loaded: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Missing descriptions: {df['Functieomschrijving'].isnull().sum()}")
        print("-----------------------\n")


def filter_jobs_by_keywords(df, keywords):
    """Filters the dataframe for jobs based on a list of keywords."""
    if df is None:
        return None

    print("Filtering for target jobs...")

    df_filtered = df.dropna(subset=["Functieomschrijving"]).copy()

    keyword_pattern = "|".join(keywords)

    mask = df_filtered["Vacaturetitel"].str.contains(
        keyword_pattern, case=False, na=False
    ) | df_filtered["Functieomschrijving"].str.contains(
        keyword_pattern, case=False, na=False
    )

    df_target = df_filtered[mask]

    print(
        f"Found {len(df_target)} potential target jobs out of {len(df_filtered)} jobs with descriptions."
    )

    return df_target


def analyze_by_category(df, analysis_title, category_dict):
    """Generic function to analyze the frequency of keywords from a dictionary."""
    if df is None or df.empty:
        print(f"No jobs to analyze for {analysis_title}.")
        return

    print(f"\n--- Analyzing {analysis_title} ---")

    search_text = (
        df["Vacaturetitel"]
        .str.cat(df["Functieomschrijving"], sep=" ", na_rep="")
        .str.lower()
    )

    counts = {}
    for category, keywords in category_dict.items():
        pattern = "|".join(keywords)
        count = search_text.str.contains(pattern, case=False).sum()
        if count > 0:
            counts[category] = count

    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    print(f"Most mentioned in {analysis_title}:")
    for item, count in sorted_counts:
        print(f"- {item}: {count}")

    print("--------------------------------" + "-" * len(analysis_title) + "\n")


def main():
    """Main function to run the analysis pipeline."""
    consolidated_file = os.path.join("data", "consolidated.csv")

    # Step 1: Load and inspect the data
    df = load_data(consolidated_file)
    inspect_data(df)

    # Step 2: Filter for target jobs using keywords from config
    df_target_jobs = filter_jobs_by_keywords(df, config.JOB_FILTER_KEYWORDS)

    if df_target_jobs is not None and not df_target_jobs.empty:
        # Step 3: Run all analyses using configurations from config.py
        analyze_by_category(df_target_jobs, "Job Tasks (RQ1)", config.JOB_TASKS)
        analyze_by_category(df_target_jobs, "Technologies (RQ2)", config.TECHNOLOGIES)
        analyze_by_category(df_target_jobs, "Soft Skills (RQ3)", config.SOFT_SKILLS)
    else:
        print("No target jobs found to analyze.")


if __name__ == "__main__":
    main()
