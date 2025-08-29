import pandas as pd
import json
import os
from tqdm import tqdm


def consolidate_analysis_results(input_dir, output_csv):
    """
    Reads all JSON files from an input directory, consolidates them,
    and saves the result as a CSV file.
    """
    all_data = []
    files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    for filename in tqdm(files, desc="Consolidating analysis files"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                # Add original filename for traceability
                data["source_file"] = filename
                all_data.append(data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {filename}")

    if not all_data:
        print("No data to consolidate.")
        return

    # Flatten the data for easier DataFrame creation
    flattened_data = []
    for entry in all_data:
        # Extract classification info
        classification_info = entry.get("classification", {})
        profile = classification_info.get("profile")
        confidence = classification_info.get("confidence")
        rationale = classification_info.get("rationale")

        # Extract thematic analysis info
        thematic_info = entry.get("thematic_analysis", {})
        job_tasks = thematic_info.get("job_tasks", [])
        technologies = thematic_info.get("technologies", [])
        soft_skills = thematic_info.get("soft_skills", [])

        # Create a record for each extracted phrase (task, tech, skill)
        # This creates a long-format dataframe which is good for analysis

        for task in job_tasks:
            flattened_data.append(
                {
                    "source_file": entry.get("source_file"),
                    "profile": profile,
                    "confidence": confidence,
                    "rationale": rationale,
                    "category_type": "job_task",
                    "category_id": task.get("category_id"),
                    "category_name": task.get("category_name"),
                    "phrase": task.get("phrase"),
                    "justification": task.get("justification"),
                }
            )

        for tech in technologies:
            flattened_data.append(
                {
                    "source_file": entry.get("source_file"),
                    "profile": profile,
                    "confidence": confidence,
                    "rationale": rationale,
                    "category_type": "technology",
                    "category_id": tech.get("category_id"),
                    "category_name": tech.get("category_name"),
                    "phrase": tech.get("phrase"),
                    "justification": None,  # Justification might not be present for all types
                }
            )

        for skill in soft_skills:
            flattened_data.append(
                {
                    "source_file": entry.get("source_file"),
                    "profile": profile,
                    "confidence": confidence,
                    "rationale": rationale,
                    "category_type": "soft_skill",
                    "category_id": skill.get("category_id"),
                    "category_name": skill.get("category_name"),
                    "phrase": skill.get("phrase"),
                    "justification": None,
                }
            )

        # If a job ad has no thematic analysis, we should still keep its classification
        if not any([job_tasks, technologies, soft_skills]):
            flattened_data.append(
                {
                    "source_file": entry.get("source_file"),
                    "profile": profile,
                    "confidence": confidence,
                    "rationale": rationale,
                    "category_type": None,
                    "category_id": None,
                    "category_name": None,
                    "phrase": None,
                    "justification": None,
                }
            )

    df = pd.DataFrame(flattened_data)

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Consolidated data saved to {output_csv}")
    print(f"Total records: {len(df)}")
    print("DataFrame columns:", df.columns.tolist())
    print("DataFrame head:\n", df.head())


if __name__ == "__main__":
    INPUT_DIRECTORY = "data/automated_analysis"
    OUTPUT_CSV = "data/automated_analysis_consolidated.csv"
    consolidate_analysis_results(INPUT_DIRECTORY, OUTPUT_CSV)
