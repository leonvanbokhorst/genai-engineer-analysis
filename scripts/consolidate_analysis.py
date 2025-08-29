import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = WORKSPACE_DIR / "data" / "automated_analysis_deduplicated"
OUTPUT_FILE = WORKSPACE_DIR / "data" / "analysis_results.csv"


def flatten_json(data, job_id):
    """
    Flattens the complex JSON structure from a single analysis file
    into a dictionary suitable for a DataFrame row.
    """
    # Extracting top-level profile and confidence info
    profile_info = data.get("profile", {})
    confidence_info = data.get("confidence", {})
    analysis_info = data.get("analysis", {})

    # Extracting and transforming nested lists of tasks, techs, and skills
    job_tasks = analysis_info.get("job_tasks", [])
    technologies = analysis_info.get("technologies", [])
    soft_skills = analysis_info.get("soft_skills", [])

    return {
        "job_id": job_id,
        "assigned_profile": profile_info.get("assigned_profile"),
        "profile_rationale": profile_info.get("rationale"),
        "confidence_score": confidence_info.get("score"),
        "confidence_reasoning": confidence_info.get("reasoning"),
        "job_tasks": json.dumps(job_tasks),  # Store the full list as a JSON string
        "technologies": json.dumps(
            technologies
        ),  # Store the full list as a JSON string
        "soft_skills": json.dumps(soft_skills),  # Store the full list as a JSON string
    }


def main():
    """
    Main function to consolidate all JSON analysis files into a single CSV.
    """
    print("--- Starting Analysis Consolidation ---")

    if not INPUT_DIR.exists():
        print(f"ERROR: Input directory not found at {INPUT_DIR}")
        return

    all_records = []
    json_files = list(INPUT_DIR.glob("analysis_job_*.json"))

    for file_path in tqdm(json_files, desc="Consolidating JSON files"):
        job_id_str = file_path.stem.split("_")[-1]
        if not job_id_str.isdigit():
            print(f"Skipping file with invalid name: {file_path.name}")
            continue

        job_id = int(job_id_str)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)

            # The actual data might be nested under an "analysis" or similar key
            # based on the sample, it seems the root is the object we need.
            if content.get("error"):
                print(
                    f"Skipping job {job_id} due to analysis error in file: {content.get('error')}"
                )
                continue

            record = flatten_json(content, job_id)
            all_records.append(record)

        except json.JSONDecodeError:
            print(f"Skipping corrupt JSON file: {file_path.name}")
        except Exception as e:
            print(f"An unexpected error occurred processing {file_path.name}: {e}")

    if not all_records:
        print("No valid records found to consolidate.")
        return

    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_records)

    # Reorder columns for better readability
    column_order = [
        "job_id",
        "assigned_profile",
        "confidence_score",
        "profile_rationale",
        "confidence_reasoning",
        "job_tasks",
        "technologies",
        "soft_skills",
    ]
    df = df[column_order]

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"\n--- Consolidation Complete ---")
    print(f"Successfully consolidated {len(df)} records.")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
