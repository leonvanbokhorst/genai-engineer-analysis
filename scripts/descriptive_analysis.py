import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def perform_descriptive_analysis(tidy_input_csv, profiles_csv, output_dir):
    """
    Performs a descriptive statistical analysis on the consolidated data.
    """
    tidy_df = pd.read_csv(tidy_input_csv)
    profiles_df = pd.read_csv(profiles_csv)

    print("--- Tidy Dataset Info ---")
    tidy_df.info()

    print("\n--- Value Counts for Profiles (per unique job) ---")
    profile_counts = profiles_df["profile"].value_counts()
    print(profile_counts)

    # Plot profile distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x=profile_counts.index, y=profile_counts.values, palette="viridis")
    plt.title("Distribution of AI Engineer Profiles")
    plt.xlabel("Profile")
    plt.ylabel("Number of Job Ads")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/profile_distribution.png")
    print(f"\nSaved profile distribution plot to {output_dir}/profile_distribution.png")

    print("\n--- Value Counts for Category Types ---")
    category_counts = tidy_df["category_type"].value_counts()
    print(category_counts)

    # Plot category type distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="plasma")
    plt.title("Distribution of Category Types")
    plt.xlabel("Category Type")
    plt.ylabel("Total Mentions (Phrases/Keywords)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_type_distribution.png")
    print(
        f"Saved category type distribution plot to {output_dir}/category_type_distribution.png"
    )

    print("\n--- Analysis of Job Tasks ---")
    job_tasks_df = tidy_df[tidy_df["category_type"] == "job_task"]
    job_task_counts = job_tasks_df["category_name"].value_counts()
    print(job_task_counts)

    # Plot job task distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=job_task_counts.index, y=job_task_counts.values, palette="magma")
    plt.title("Distribution of Job Tasks")
    plt.xlabel("Job Task")
    plt.ylabel("Total Mentions (Phrases)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/job_task_distribution.png")
    print(f"Saved job task distribution plot to {output_dir}/job_task_distribution.png")

    print("\n--- Analysis of Technologies ---")

    technologies_df = tidy_df[tidy_df["category_type"] == "technology"].copy()

    # Count by category_name as category_id might be missing
    tech_counts = technologies_df["category_name"].value_counts().head(20)  # Top 20
    print(tech_counts)

    # Plot technology distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=tech_counts.index, y=tech_counts.values, palette="cubehelix")
    plt.title("Top 20 Most Frequent Technologies")
    plt.xlabel("Technology Category")
    plt.ylabel("Total Mentions (Tools)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/technology_distribution.png")
    print(
        f"Saved technology distribution plot to {output_dir}/technology_distribution.png"
    )

    print("\n--- Analysis of Soft Skills ---")
    soft_skills_df = tidy_df[tidy_df["category_type"] == "soft_skill"]
    skill_counts = soft_skills_df["category_name"].value_counts()
    print(skill_counts)

    # Plot soft skill distribution
    plt.figure(figsize=(12, 8))
    sns.barplot(x=skill_counts.index, y=skill_counts.values, palette="rocket")
    plt.title("Distribution of Soft Skills")
    plt.xlabel("Soft Skill")
    plt.ylabel("Total Mentions (Phrases)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/soft_skill_distribution.png")
    print(
        f"Saved soft skill distribution plot to {output_dir}/soft_skill_distribution.png"
    )


def compute_top_tools(tidy_df_path, profiles_df_path, output_dir):
    """Computes the top tools overall and per profile."""
    df_tidy = pd.read_csv(tidy_df_path)
    df_profiles = pd.read_csv(profiles_df_path)

    tech_df = df_tidy[df_tidy["category_type"] == "technology"].copy()

    # --- Top Tools Overall ---
    # Ensure tool_name column has string values before using .str accessor
    if pd.api.types.is_string_dtype(tech_df["tool_name"]):
        valid_tools = tech_df[
            pd.notna(tech_df["tool_name"]) & (tech_df["tool_name"].str.strip() != "")
        ]
        top_tools_overall = valid_tools["tool_name"].value_counts().reset_index()
        top_tools_overall.columns = ["Tool", "Frequency"]
        top_tools_overall.to_csv(output_dir / "top_tools_overall.csv", index=False)
    else:
        # Create an empty file if there are no tools to analyze
        pd.DataFrame(columns=["Tool", "Frequency"]).to_csv(
            output_dir / "top_tools_overall.csv", index=False
        )

    # --- Top Tools by Profile ---
    merged_df = pd.merge(tech_df, df_profiles, on="job_id")
    if pd.api.types.is_string_dtype(merged_df["tool_name"]):
        valid_tools_by_profile = merged_df[
            pd.notna(merged_df["tool_name"])
            & (merged_df["tool_name"].str.strip() != "")
        ]

        top_tools_by_profile = (
            valid_tools_by_profile.groupby("profile")["tool_name"]
            .value_counts()
            .groupby(level=0)
            .head(10)
            .reset_index(name="Frequency")
        )
        top_tools_by_profile.to_csv(
            output_dir / "top_tools_by_profile.csv", index=False
        )
    else:
        # Create an empty file
        pd.DataFrame(columns=["profile", "tool_name", "Frequency"]).to_csv(
            output_dir / "top_tools_by_profile.csv", index=False
        )


def derive_focus_rq1b(tidy_input_csv, output_dir):
    """
    Derive focus per job based on presence of TASK3 (Modeling) and TASK4 (Software Development).
    Focus categories: Data Science, Software Engineering, Data Science & Software Engineering, No info
    Saves: focus_by_job.csv and focus_distribution.png
    """
    tidy_df = pd.read_csv(tidy_input_csv)
    tasks = tidy_df[tidy_df["category_type"] == "job_task"][
        ["job_id", "category_name"]
    ].copy()

    # Presence flags per job
    modeling = (
        tasks.assign(
            is_modeling=tasks["category_name"].str.contains("Modeling", na=False)
        )
        .groupby("job_id")["is_modeling"]
        .any()
    )
    software = (
        tasks.assign(
            is_software=tasks["category_name"].str.contains(
                "Software Development", na=False
            )
        )
        .groupby("job_id")["is_software"]
        .any()
    )

    jobs = (
        pd.DataFrame({"modeling": modeling, "software": software})
        .fillna(False)
        .reset_index()
    )

    def label_focus(row):
        if row["modeling"] and row["software"]:
            return "Data Science & Software Engineering"
        if row["modeling"] and not row["software"]:
            return "Data Science"
        if row["software"] and not row["modeling"]:
            return "Software Engineering"
        return "No info"

    jobs["focus"] = jobs.apply(label_focus, axis=1)
    jobs[["job_id", "focus"]].to_csv(
        f"{output_dir}/focus_by_job.csv", index=False, encoding="utf-8"
    )
    print(f"Saved per-job focus labels to {output_dir}/focus_by_job.csv")

    # Plot distribution
    focus_counts = jobs["focus"].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=focus_counts.index, y=focus_counts.values, palette="crest")
    plt.title("Focus per Job (RQ1b)")
    plt.xlabel("Focus Category")
    plt.ylabel("Number of Job Ads")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/focus_distribution.png")
    print(f"Saved focus distribution plot to {output_dir}/focus_distribution.png")


def job_task_coverage_per_job(tidy_input_csv, output_dir):
    """
    Count, for each job task category, how many unique job ads mention it at least once.
    Saves: job_task_jobs_counts.csv and job_task_jobs_distribution.png
    """
    tidy_df = pd.read_csv(tidy_input_csv)
    tasks = tidy_df[tidy_df["category_type"] == "job_task"][
        ["job_id", "category_name"]
    ].dropna()

    unique_pairs = tasks.drop_duplicates()
    counts = unique_pairs["category_name"].value_counts()

    # Save CSV
    counts.reset_index().rename(
        columns={"index": "category_name", "category_name": "num_jobs"}
    ).to_csv(f"{output_dir}/job_task_jobs_counts.csv", index=False, encoding="utf-8")
    print(f"Saved job-task per-job counts to {output_dir}/job_task_jobs_counts.csv")

    # Plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x=counts.index, y=counts.values, palette="viridis")
    plt.title("Jobs Mentioning Each Task At Least Once")
    plt.xlabel("Job Task")
    plt.ylabel("Number of Job Ads")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/job_task_jobs_distribution.png")
    print(
        f"Saved per-job job-task distribution plot to {output_dir}/job_task_jobs_distribution.png"
    )


def perform_profile_analysis(tidy_input_csv, profiles_csv):
    """
    Analyzes the skills and technologies associated with each engineer profile.
    """
    tidy_df = pd.read_csv(tidy_input_csv)
    profiles_df = pd.read_csv(profiles_csv)
    df = tidy_df.merge(profiles_df, on="job_id", how="left")

    # Filter for relevant profiles
    profiles = ["GenAI Engineer", "ML Engineer"]
    df_filtered = df[df["profile"].isin(profiles)]

    print("\n--- Cross-Tabulation: Profiles vs. Job Tasks ---")
    task_profile_ct = pd.crosstab(df_filtered["category_name"], df_filtered["profile"])
    print(task_profile_ct)

    print("\n--- Cross-Tabulation: Profiles vs. Technologies ---")
    technologies_df = df_filtered[df_filtered["category_type"] == "technology"].copy()
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
    # --- File Paths ---
    INPUT_TIDY_CSV = Path("data/automated_analysis_consolidated.csv")
    INPUT_PROFILES_CSV = Path("data/automated_analysis_profiles.csv")
    OUTPUT_DIR = Path("data/analysis_results")

    OUTPUT_DIR.mkdir(exist_ok=True)
    perform_descriptive_analysis(INPUT_TIDY_CSV, INPUT_PROFILES_CSV, OUTPUT_DIR)
    compute_top_tools(INPUT_TIDY_CSV, INPUT_PROFILES_CSV, OUTPUT_DIR)
    derive_focus_rq1b(INPUT_TIDY_CSV, OUTPUT_DIR)
    job_task_coverage_per_job(INPUT_TIDY_CSV, OUTPUT_DIR)
    perform_profile_analysis(INPUT_TIDY_CSV, INPUT_PROFILES_CSV)
