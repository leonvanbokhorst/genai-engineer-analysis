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
    """Analyzes and visualizes the co-occurrence of the top 20 technologies."""
    print("\n--- Performing Technology Co-occurrence Analysis ---")
    tech_df = tidy_df[tidy_df["category_type"] == "technology"].copy()

    if "tool_name" not in tech_df.columns or tech_df["tool_name"].isnull().all():
        print(
            "Skipping technology co-occurrence analysis: 'tool_name' column is missing or empty."
        )
        fig, ax = plt.subplots()
        ax.set_title("Technology Co-occurrence (No Data)")
        plt.savefig(
            OUTPUT_DIR / "technology_cooccurrence_heatmap.png", bbox_inches="tight"
        )
        return

    tech_df.dropna(subset=["tool_name"], inplace=True)

    # Normalize tool names
    def normalize_tool_name(name: str) -> str:
        name = str(name).strip().lower()
        synonyms = {
            "open ai": "OpenAI",
            "openai": "OpenAI",
            "azure openai": "Azure OpenAI",
            "ms azure": "Azure",
            "microsoft azure": "Azure",
            "azure": "Azure",
            "amazon web services": "AWS",
            "aws": "AWS",
            "gcp": "GCP",
            "google cloud": "GCP",
            "google cloud platform": "GCP",
            "k8s": "Kubernetes",
            "kubernetes": "Kubernetes",
            "docker": "Docker",
            "git": "Git",
            "langchain": "LangChain",
            "huggingface": "Hugging Face",
            "hugging face": "Hugging Face",
            "mlflow": "MLflow",
            "faiss": "FAISS",
            "pinecone": "Pinecone",
            "chromadb": "ChromaDB",
            "postgres": "PostgreSQL",
            "postgresql": "PostgreSQL",
            "sql": "SQL",
            "tensorflow": "TensorFlow",
            "tf": "TensorFlow",
            "pytorch": "PyTorch",
            "scikit-learn": "scikit-learn",
            "sklearn": "scikit-learn",
            "apache airflow": "Airflow",
            "airflow": "Airflow",
            "vertex ai": "Vertex AI",
            "anthropic": "Anthropic",
            "claude": "Claude",
            "gpt-4": "GPT-4",
            "gpt4": "GPT-4",
            "gpt": "GPT",
            "llama": "Llama",
            "llama 3": "Llama",
            "llm": "LLMs",
            "llms": "LLMs",
            "large language models": "LLMs",
            "mistral": "Mistral",
            "databricks": "Databricks",
            "power bi": "Power BI",
            "ai": "AI",
            "genai": "AI",
            "generative ai": "AI",
            "machine learning": "Machine Learning",
        }
        return synonyms.get(name, str(name).strip().title())

    tech_df["tool_name"] = tech_df["tool_name"].apply(normalize_tool_name)

    # Get the top 20 most frequent tools
    top_tools = tech_df["tool_name"].value_counts().nlargest(20).index.tolist()
    tech_df_top = tech_df[tech_df["tool_name"].isin(top_tools)]

    # Create a matrix of jobs and their technologies
    job_tool_matrix = tech_df_top.pivot_table(
        index="job_id", columns="tool_name", aggfunc="size", fill_value=0
    )

    # Convert to binary (presence/absence)
    job_tool_matrix[job_tool_matrix > 1] = 1

    # Calculate the co-occurrence matrix
    co_occurrence_matrix = job_tool_matrix.T.dot(job_tool_matrix)
    # Set the diagonal to zero to improve visualization
    np.fill_diagonal(co_occurrence_matrix.values, 0)

    # Plot the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        co_occurrence_matrix,
        cmap="viridis",
        annot=False,
    )
    plt.title("Co-occurrence Matrix of Top 20 Technologies")
    plt.xlabel("Technology")
    plt.ylabel("Technology")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "technology_cooccurrence_heatmap.png", bbox_inches="tight")
    print(
        f"Saved technology co-occurrence heatmap to {OUTPUT_DIR / 'technology_cooccurrence_heatmap.png'}"
    )


def generate_normalized_crosstabs(tidy_df, profiles_df):
    """Generates and saves normalized crosstabs for all category types."""
    print("\n--- Generating Normalized Cross-Tabulations ---")

    # Merge profiles into the tidy dataframe first
    df = pd.merge(tidy_df, profiles_df, on="job_id", how="left")
    df_filtered = df[df["profile"].isin(PROFILES_TO_COMPARE)]

    category_types = ["job_task", "technology", "soft_skill"]
    for cat_type in category_types:
        category_df = df_filtered[df_filtered["category_type"] == cat_type].copy()

        # Some old cleaning logic might still be trying to use tool_name
        if "tool_name" in category_df.columns and pd.api.types.is_string_dtype(
            category_df["tool_name"]
        ):
            category_df = category_df[
                ~category_df["tool_name"].str.contains(r"^TECH\d*:", na=False)
            ]

        save_normalized_crosstab(
            category_df,
            cat_type,
            f"normalized_crosstab_{cat_type}.csv",
        )


def save_normalized_crosstab(category_df, category_type, output_name):
    """
    Generates and saves normalized (percentage-based) cross-tabulations for each
    category type by profile.
    """
    if category_df.empty:
        print(f"Skipping normalized crosstab for {category_type} due to no data.")
        # Create an empty file to avoid downstream errors
        output_path = OUTPUT_DIR / output_name
        pd.DataFrame().to_csv(output_path)
        print(f"Saved empty crosstab for {category_type} to {output_path}")
        return

    crosstab = pd.crosstab(
        category_df["category_name"],
        category_df["profile"],
    )

    if crosstab.empty:
        print(f"Skipping normalized crosstab for {category_type} as crosstab is empty.")
        # Create an empty file to avoid downstream errors
        output_path = OUTPUT_DIR / output_name
        pd.DataFrame().to_csv(output_path)
        print(f"Saved empty crosstab for {category_type} to {output_path}")
        return

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
    output_path = OUTPUT_DIR / output_name
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
