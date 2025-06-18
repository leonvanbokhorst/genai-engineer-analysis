import pandas as pd
import os
import config  # Import our new configuration file
import re


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


def find_context_for_keywords(df, keywords_to_find, context_window=100):
    """Finds and prints the context for specific keywords in job descriptions."""
    if df is None or df.empty:
        print("No jobs to analyze for keyword context.")
        return

    print(f"\n--- Context Analysis for: {', '.join(keywords_to_find)} ---")

    # Combine job title and description for search
    search_text_series = df["Functieomschrijving"]

    for keyword in keywords_to_find:
        print(f"\n--- Occurrences of '{keyword}' ---")
        found_count = 0
        # Create a regex pattern to find the keyword (case-insensitive)
        # Using word boundaries to avoid matching parts of words
        pattern = re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)

        for index, text in search_text_series.items():
            if not isinstance(text, str):
                continue

            # Find all matches in the text
            for match in pattern.finditer(text):
                found_count += 1
                start, end = match.start(), match.end()

                # Extract context window around the match
                start_context = max(0, start - context_window)
                end_context = min(len(text), end + context_window)
                context = text[start_context:end_context]

                # Highlight the keyword in the context
                highlighted_context = pattern.sub(f">>>{match.group(0)}<<<", context)

                print(f"Job Ad Index {index}: ...{highlighted_context}...")
                # Limit the number of examples printed per keyword
                if found_count >= 5:
                    break
            if found_count >= 5:
                break

        if found_count == 0:
            print("No occurrences found.")
        elif found_count >= 5:
            print("...and more.")


def assess_filter_keywords(df, current_keywords):
    """
    Analyzes the effectiveness of the current filter keywords and suggests new ones
    by searching the entire dataset.
    """
    if df is None or df.empty:
        print("No jobs to analyze.")
        return

    print("\n--- Assessing Job Filter Keywords ---")

    search_text = (
        df["Vacaturetitel"]
        .str.cat(df["Functieomschrijving"], sep=" ", na_rep="")
        .str.lower()
    )

    # 1. Analyze hit counts for current keywords
    print("\n--- Hit Count for Current Keywords ---")
    keyword_counts = {}
    for keyword in current_keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        count = search_text.str.contains(pattern, case=False, na=False).sum()
        if count > 0:
            keyword_counts[keyword] = count

    sorted_keywords = sorted(
        keyword_counts.items(), key=lambda item: item[1], reverse=True
    )

    print("Mentions for each keyword in the current filter:")
    for keyword, count in sorted_keywords:
        print(f"- '{keyword}': {count} mentions")

    # 2. Suggest potential new keywords
    print("\n--- Suggestions for New Keywords ---")

    potential_new_keywords = [
        "claude",
        "anthropic",
        "gemini",
        "mistral",
        "cohere",  # Other Models/Companies
        "haystack",
        "sentence transformers",
        "fastapi",  # Other Libraries/Tools
        "vector search",
        "semantic search",  # Other Concepts
        "natural language processing",
        "nlp",
        "computer vision",
    ]

    new_keyword_suggestions = [
        k for k in potential_new_keywords if k not in current_keywords
    ]

    new_keyword_counts = {}
    for keyword in new_keyword_suggestions:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        count = search_text.str.contains(pattern, case=False, na=False).sum()
        if count > 0:
            new_keyword_counts[keyword] = count

    if not new_keyword_counts:
        print("No occurrences found for suggested new keywords.")
    else:
        sorted_new_keywords = sorted(
            new_keyword_counts.items(), key=lambda item: item[1], reverse=True
        )
        print(
            "Found mentions for these potential new keywords (not currently in filter):"
        )
        for keyword, count in sorted_new_keywords:
            print(f"- '{keyword}': {count} mentions")

    print("\n-------------------------------------\n")


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
