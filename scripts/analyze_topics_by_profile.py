import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSPACE_DIR / "data"
ANALYSIS_RESULTS_DIR = WORKSPACE_DIR / "data" / "analysis_results"
INPUT_PROFILES_CSV = DATA_DIR / "automated_analysis_profiles.csv"
INPUT_TOPIC_MAPPING_CSV = ANALYSIS_RESULTS_DIR / "job_topic_mapping.csv"
INPUT_TOPIC_DEFS_CSV = ANALYSIS_RESULTS_DIR / "topic_definitions.csv"
OUTPUT_CROSSTAB_CSV = ANALYSIS_RESULTS_DIR / "crosstab_profiles_vs_topics.csv"
OUTPUT_HEATMAP_PNG = ANALYSIS_RESULTS_DIR / "heatmap_profiles_vs_topics.png"


def analyze_topics_by_profile():
    """
    Merges job profiles with their dominant topics and creates a crosstab and heatmap
    to visualize the relationship between them.
    """
    print("Loading datasets...")
    profiles_df = pd.read_csv(INPUT_PROFILES_CSV)
    topic_mapping_df = pd.read_csv(INPUT_TOPIC_MAPPING_CSV)
    topic_defs_df = pd.read_csv(INPUT_TOPIC_DEFS_CSV)

    # Clean up topic definitions for better labels
    # Example: "student | frontend | ..." -> "T0: student, frontend"
    topic_defs_df["short_label"] = topic_defs_df.apply(
        lambda row: f"T{row['topic_id']}: "
        + ", ".join(row["top_words"].split(" | ")[:2]),
        axis=1,
    )
    topic_labels = topic_defs_df.set_index("topic_id")["short_label"].to_dict()

    print("Merging dataframes...")
    # The topic mapping is based on the index of the original dataframe, which corresponds to job_id
    # Ensure job_id is of the same type if merging directly
    # The topic modeling script saves the index as job_id, so a direct merge should work.
    merged_df = pd.merge(profiles_df, topic_mapping_df, on="job_id", how="inner")

    # Filter out ambiguous profiles for a clearer analysis
    merged_df = merged_df[~merged_df["profile"].str.contains("Ambiguous", na=False)]

    print("Creating cross-tabulation of profiles vs. topics...")
    crosstab = pd.crosstab(merged_df["profile"], merged_df["dominant_topic"])

    # Normalize the crosstab to show percentages (row-wise)
    crosstab_norm = crosstab.div(crosstab.sum(axis=1), axis=0) * 100

    # Map topic IDs to short labels for readability in the plot
    crosstab_norm.columns = crosstab_norm.columns.map(topic_labels)
    crosstab.columns = crosstab.columns.map(topic_labels)

    # Save the raw count crosstab to CSV
    crosstab.to_csv(OUTPUT_CROSSTAB_CSV)
    print(f"Saved crosstab to {OUTPUT_CROSSTAB_CSV}")

    print("Generating and saving heatmap...")
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        crosstab_norm,
        annot=True,
        fmt=".1f",
        cmap="viridis",
        linewidths=0.5,
        cbar_kws={"label": "% of Jobs in Profile"},
    )
    plt.title("Heatmap of Topic Distribution within each AI Engineer Profile")
    plt.xlabel("Dominant Topic")
    plt.ylabel("Job Profile")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_HEATMAP_PNG)
    print(f"Saved heatmap to {OUTPUT_HEATMAP_PNG}")


if __name__ == "__main__":
    analyze_topics_by_profile()
