import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def perform_descriptive_analysis(input_csv, output_dir):
    """
    Performs a descriptive statistical analysis on the consolidated data.
    """
    df = pd.read_csv(input_csv)

    print("--- Dataset Info ---")
    df.info()

    print("\n--- Value Counts for Profiles ---")
    profile_counts = df["profile"].value_counts()
    print(profile_counts)

    # Plot profile distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x=profile_counts.index, y=profile_counts.values, palette="viridis")
    plt.title("Distribution of AI Engineer Profiles")
    plt.xlabel("Profile")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/profile_distribution.png")
    print(f"\nSaved profile distribution plot to {output_dir}/profile_distribution.png")

    print("\n--- Value Counts for Category Types ---")
    category_counts = df["category_type"].value_counts()
    print(category_counts)

    # Plot category type distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="plasma")
    plt.title("Distribution of Category Types")
    plt.xlabel("Category Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_type_distribution.png")
    print(
        f"Saved category type distribution plot to {output_dir}/category_type_distribution.png"
    )

    print("\n--- Analysis of Job Tasks ---")
    job_tasks_df = df[df["category_type"] == "job_task"]
    job_task_counts = job_tasks_df["category_name"].value_counts()
    print(job_task_counts)

    # Plot job task distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=job_task_counts.index, y=job_task_counts.values, palette="magma")
    plt.title("Distribution of Job Tasks")
    plt.xlabel("Job Task")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/job_task_distribution.png")
    print(f"Saved job task distribution plot to {output_dir}/job_task_distribution.png")

    print("\n--- Analysis of Technologies ---")

    tech_mapping = {
        "TECH1": "Programming Languages",
        "TECH2": "Cloud Platforms & Services",
        "TECH3": "LLM / Generative Models",
        "TECH4": "LLM Frameworks & Libraries",
        "TECH5": "Vector Stores & Search",
        "TECH6": "MLOps & Data Pipelines",
        "TECH7": "Data Visualization",
        "TECH8": "Data Processing",
        "TECH9": "Data Storage",
        "TECH10": "Data Modeling",
        "TECH11": "Data Analysis",
    }

    technologies_df = df[df["category_type"] == "technology"].copy()
    technologies_df["category_name"] = technologies_df["category_id"].map(tech_mapping)

    # Count by category_id as category_name might be missing
    tech_counts = technologies_df["category_name"].value_counts().head(20)  # Top 20
    print(tech_counts)

    # Plot technology distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=tech_counts.index, y=tech_counts.values, palette="cubehelix")
    plt.title("Top 20 Most Frequent Technologies")
    plt.xlabel("Technology Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/technology_distribution.png")
    print(
        f"Saved technology distribution plot to {output_dir}/technology_distribution.png"
    )

    print("\n--- Analysis of Soft Skills ---")
    soft_skills_df = df[df["category_type"] == "soft_skill"]
    skill_counts = soft_skills_df["category_name"].value_counts()
    print(skill_counts)

    # Plot soft skill distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=skill_counts.index, y=skill_counts.values, palette="rocket")
    plt.title("Distribution of Soft Skills")
    plt.xlabel("Soft Skill")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/soft_skill_distribution.png")
    print(
        f"Saved soft skill distribution plot to {output_dir}/soft_skill_distribution.png"
    )


def perform_profile_analysis(input_csv):
    """
    Analyzes the skills and technologies associated with each engineer profile.
    """
    df = pd.read_csv(input_csv)

    # Filter for relevant profiles
    profiles = ["GenAI Engineer", "ML Engineer"]
    df_filtered = df[df["profile"].isin(profiles)]

    print("\n--- Cross-Tabulation: Profiles vs. Job Tasks ---")
    task_profile_ct = pd.crosstab(df_filtered["category_name"], df_filtered["profile"])
    print(task_profile_ct)

    print("\n--- Cross-Tabulation: Profiles vs. Technologies ---")
    tech_mapping = {
        "TECH1": "Programming Languages",
        "TECH2": "Cloud Platforms & Services",
        "TECH3": "LLM / Generative Models",
        "TECH4": "LLM Frameworks & Libraries",
        "TECH5": "Vector Stores & Search",
        "TECH6": "MLOps & Data Pipelines",
        "TECH7": "Data Visualization",
        "TECH8": "Data Processing",
        "TECH9": "Data Storage",
        "TECH10": "Data Modeling",
        "TECH11": "Data Analysis",
    }
    technologies_df = df_filtered[df_filtered["category_type"] == "technology"].copy()
    technologies_df["category_name"] = technologies_df["category_id"].map(tech_mapping)
    tech_profile_ct = pd.crosstab(
        technologies_df["category_name"], technologies_df["profile"]
    )
    print(tech_profile_ct)

    print("\n--- Cross-Tabulation: Profiles vs. Soft Skills ---")
    soft_skills_df = df_filtered[df_filtered["category_type"] == "soft_skill"]
    skill_profile_ct = pd.crosstab(
        soft_skills_df["category_name"], soft_skills_df["profile"]
    )
    print(skill_profile_ct)


if __name__ == "__main__":
    INPUT_CSV = "data/automated_analysis_consolidated.csv"
    OUTPUT_DIR = "data/analysis_results"
    import os

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    perform_descriptive_analysis(INPUT_CSV, OUTPUT_DIR)
    perform_profile_analysis(INPUT_CSV)
