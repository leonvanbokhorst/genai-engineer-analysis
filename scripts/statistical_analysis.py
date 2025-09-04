import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from pathlib import Path
import itertools

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
INPUT_TIDY_CSV = WORKSPACE_DIR / "data" / "automated_analysis_consolidated.csv"
INPUT_PROFILES_CSV = WORKSPACE_DIR / "data" / "automated_analysis_profiles.csv"
OUTPUT_DIR = WORKSPACE_DIR / "data" / "analysis_results"
PROFILES_TO_COMPARE = ["GenAI Engineer", "ML Engineer"]


def perform_chi_squared_tests(tidy_df, profiles_df):
    """
    Performs Chi-Squared tests for job_tasks, technologies, and soft_skills
    between GenAI and ML Engineer profiles.
    """
    print("\n--- Performing Chi-Squared Tests ---")
    df = tidy_df.merge(profiles_df, on="job_id", how="left")
    df_filtered = df[df["profile"].isin(PROFILES_TO_COMPARE)]

    results = []

    for category_type in ["job_task", "technology", "soft_skill"]:
        contingency_table = pd.crosstab(
            df_filtered[df_filtered["category_type"] == category_type]["category_name"],
            df_filtered[df_filtered["category_type"] == category_type]["profile"],
        )

        if contingency_table.empty or contingency_table.shape[0] < 2:
            print(
                f"Skipping Chi-Squared test for {category_type} due to insufficient data."
            )
            continue

        chi2, p, _, _ = chi2_contingency(contingency_table)
        results.append(
            {"category_type": category_type, "chi2_statistic": chi2, "p_value": p}
        )
        print(f"Chi-Squared Test for {category_type}: p-value = {p:.4f}")

    results_df = pd.DataFrame(results)
    output_path = OUTPUT_DIR / "chi_squared_results.csv"
    results_df.to_csv(output_path, index=False)
    print(f"Saved Chi-Squared test results to {output_path}")
    return results_df


def technology_cooccurrence_analysis(tidy_df):
    """
    Analyzes and visualizes the co-occurrence of the top 20 technologies.
    """
    print("\n--- Performing Technology Co-occurrence Analysis ---")
    tech_df = tidy_df[tidy_df["category_type"] == "technology"].copy()
    tech_df.dropna(subset=["tool_name"], inplace=True)

    # Get the top 20 most frequent tools
    top_tools = tech_df["tool_name"].value_counts().nlargest(20).index.tolist()
    tech_df_top = tech_df[tech_df["tool_name"].isin(top_tools)]

    # Create a matrix of jobs and their technologies
    job_tool_matrix = tech_df_top.pivot_table(
        index="job_id", columns="tool_name", aggfunc="size", fill_value=0
    )
    job_tool_matrix[job_tool_matrix > 1] = 1  # Binarize

    # Calculate co-occurrence matrix
    cooccurrence_matrix = job_tool_matrix.T.dot(job_tool_matrix)
    np.fill_diagonal(cooccurrence_matrix.values, 0)  # Remove self-co-occurrence

    # Plot heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(cooccurrence_matrix, cmap="viridis", annot=False)
    plt.title("Co-occurrence Matrix of Top 20 Technologies")
    plt.tight_layout()
    output_path = OUTPUT_DIR / "technology_cooccurrence_heatmap.png"
    plt.savefig(output_path)
    print(f"Saved technology co-occurrence heatmap to {output_path}")


def generate_normalized_crosstabs(tidy_df, profiles_df):
    """
    Generates normalized (percentage-based) cross-tabulations for each
    category type by profile.
    """
    print("\n--- Generating Normalized Cross-Tabulations ---")
    df = tidy_df.merge(profiles_df, on="job_id", how="left")
    df_filtered = df[df["profile"].isin(PROFILES_TO_COMPARE)]

    for category_type in ["job_task", "technology", "soft_skill"]:
        # Use 'tool_name' for technology, otherwise 'category_name'
        if category_type == "technology":
            column_to_crosstab = "tool_name"
            # Filter out rows where tool_name is NaN, as it can't be grouped
            category_df = df_filtered[
                df_filtered["category_type"] == category_type
            ].dropna(subset=[column_to_crosstab])
        else:
            column_to_crosstab = "category_name"
            category_df = df_filtered[df_filtered["category_type"] == category_type]

        if category_df.empty:
            print(f"Skipping normalized crosstab for {category_type} due to no data.")
            continue

        crosstab = pd.crosstab(
            category_df[column_to_crosstab],
            category_df["profile"],
        )

        if crosstab.empty:
            print(
                f"Skipping normalized crosstab for {category_type} as crosstab is empty."
            )
            # Create an empty file to avoid downstream errors
            output_path = OUTPUT_DIR / f"normalized_crosstab_{category_type}.csv"
            pd.DataFrame().to_csv(output_path)
            print(f"Saved empty crosstab for {category_type} to {output_path}")
            continue

        # --- Filter for significant technologies ---
        if category_type == "technology":
            # A technology is significant if it's mentioned at least 10 times in total
            significance_threshold = 10
            total_mentions = crosstab.sum(axis=1)
            significant_techs = total_mentions[
                total_mentions >= significance_threshold
            ].index
            crosstab = crosstab.loc[significant_techs]
            print(
                f"-> Filtered for technologies with at least {significance_threshold} mentions. Kept {len(significant_techs)} technologies."
            )

        # Normalize by column (profile)
        crosstab_norm = crosstab.div(crosstab.sum(axis=0), axis=1).mul(100).round(2)
        output_path = OUTPUT_DIR / f"normalized_crosstab_{category_type}.csv"
        crosstab_norm.to_csv(output_path)
        print(f"Saved normalized cross-tabulation for {category_type} to {output_path}")


def analyze_topic_profile_correlation():
    """
    Analyzes the correlation between discovered topics and job profiles.
    Prints a cross-tabulation showing the distribution.
    """
    print("\n--- Analyzing Topic-Profile Correlation ---")

    # Load necessary files
    try:
        profiles_df = pd.read_csv(INPUT_PROFILES_CSV)
        topics_df = pd.read_csv(OUTPUT_DIR / "job_topic_mapping.csv")
        topic_defs_df = pd.read_csv(OUTPUT_DIR / "topic_definitions.csv").set_index(
            "topic_id"
        )
    except FileNotFoundError as e:
        print(f"Error: Could not find required file. {e}")
        print("Please ensure topic_modeling.py has been run successfully.")
        return

    # Merge the dataframes
    merged_df = pd.merge(profiles_df, topics_df, on="job_id", how="inner")

    # --- Filter out non-dominant topics ---
    topic_counts = merged_df["dominant_topic"].value_counts()
    # A topic is considered non-dominant if it appears in fewer than 10 documents
    threshold = 10
    non_dominant_topics = topic_counts[topic_counts < threshold].index

    if not non_dominant_topics.empty:
        print(f"--- Filtering Non-Dominant Topics (threshold < {threshold} jobs) ---")
        print(f"Removing the following topics: {list(non_dominant_topics)}")
        merged_df = merged_df[~merged_df["dominant_topic"].isin(non_dominant_topics)]

    # Create the cross-tabulation
    correlation_table = pd.crosstab(
        merged_df["dominant_topic"],
        merged_df["profile"],
    )

    # --- Exclude specified columns ---
    cols_to_drop = ["Data Engineer", "Data Engineering"]
    existing_cols_to_drop = [
        col for col in cols_to_drop if col in correlation_table.columns
    ]
    correlation_table = correlation_table.drop(columns=existing_cols_to_drop)

    # Add the topic keywords for context
    correlation_table_with_defs = correlation_table.join(topic_defs_df)

    print("Distribution of Profiles across Discovered Topics:")
    print(correlation_table_with_defs.to_markdown())

    # Save to file
    output_path = OUTPUT_DIR / "topic_profile_correlation.md"
    correlation_table_with_defs.to_markdown(output_path)
    print(f"\nSaved topic-profile correlation table to {output_path}")


def main():
    """
    Main function to run all statistical analyses.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    tidy_df = pd.read_csv(INPUT_TIDY_CSV)
    profiles_df = pd.read_csv(INPUT_PROFILES_CSV)

    perform_chi_squared_tests(tidy_df.copy(), profiles_df.copy())
    technology_cooccurrence_analysis(tidy_df.copy())
    generate_normalized_crosstabs(tidy_df.copy(), profiles_df.copy())
    analyze_topic_profile_correlation()

    print("\n--- Statistical Analysis Complete ---")


if __name__ == "__main__":
    main()
