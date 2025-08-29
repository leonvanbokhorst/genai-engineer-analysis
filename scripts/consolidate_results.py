import os
import json
import pandas as pd
from tqdm import tqdm
import re

# Configuration
INPUT_DIR = "data/automated_analysis"
ORIGINAL_DATA_FILE = "data/consolidated_deduplicated.csv"
CODING_BOOK_FILE = "CODING_BOOK.md"
OUTPUT_FILE = "data/analysis_results_tidy.csv"


def parse_coding_book(file_path):
    """Parses the coding book to extract category names and descriptions."""
    categories = {}
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex for tasks and skills: **`ID: Name`**: Description
    pattern = re.compile(r"\*\*`([A-Z]+[0-9]+):\s*(.*?)`\*\*:\s*(.*)")
    matches = pattern.findall(content)
    for match in matches:
        cat_id, name, desc = match
        categories[cat_id] = {"name": name.strip(), "description": desc.strip()}

    # Regex for technologies: `ID: Name` (e.g., ...)
    pattern = re.compile(r"`([A-Z]+[0-9]+):\s*(.*?)`")
    matches = pattern.findall(content)
    for match in matches:
        cat_id, name = match
        if cat_id not in categories:
            categories[cat_id] = {"name": name.strip(), "description": name.strip()}

    return categories


def main():
    """Consolidates all analysis JSON files into a single, tidy CSV file."""
    if not os.path.isdir(INPUT_DIR):
        print(f"Error: Input directory not found at '{INPUT_DIR}'")
        return

    # 1. Parse the coding book
    coding_book_data = parse_coding_book(CODING_BOOK_FILE)

    # 2. Load the original data
    original_df = pd.read_csv(ORIGINAL_DATA_FILE)

    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    if not json_files:
        print(f"No JSON files found in '{INPUT_DIR}'.")
        return

    print(f"Found {len(json_files)} JSON files to consolidate into a tidy format.")

    all_rows = []

    for file_name in tqdm(json_files, desc="Consolidating Tidy Results"):
        file_path = os.path.join(INPUT_DIR, file_name)
        job_id = int(file_name.replace("analysis_", "").replace(".json", ""))

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {file_name}. Skipping.")
                continue

        # Get job-level info
        classification = data.get("classification", {})
        original_job_info = original_df.iloc[job_id]

        # Base info for all rows for this job
        base_info = {
            "job_id": job_id,
            "original_title": original_job_info.get("Vacaturetitel"),
            "original_description": original_job_info.get("Functieomschrijving"),
            "final_profile": classification.get("profile"),
            "final_confidence": classification.get("confidence"),
            "final_rationale": classification.get("rationale"),
        }

        # Unpack thematic analysis
        thematic_analysis = data.get("thematic_analysis", {})

        for task in thematic_analysis.get("job_tasks", []):
            cat_id = task.get("category_id")
            row = {
                **base_info,
                "item_type": "job_task",
                "item_category_id": cat_id,
                "item_category_name": coding_book_data.get(cat_id, {}).get("name"),
                "item_category_description": coding_book_data.get(cat_id, {}).get(
                    "description"
                ),
                "item_phrase_or_tool": task.get("phrase"),
                "item_justification": task.get("justification"),
            }
            all_rows.append(row)

        for tech in thematic_analysis.get("technologies", []):
            cat_id = tech.get("category_id")
            row = {
                **base_info,
                "item_type": "technology",
                "item_category_id": cat_id,
                "item_category_name": coding_book_data.get(cat_id, {}).get("name"),
                "item_category_description": coding_book_data.get(cat_id, {}).get(
                    "description"
                ),
                "item_phrase_or_tool": tech.get("tool_name"),
                "item_justification": None,
            }
            all_rows.append(row)

        for skill in thematic_analysis.get("soft_skills", []):
            cat_id = skill.get("category_id")
            row = {
                **base_info,
                "item_type": "soft_skill",
                "item_category_id": cat_id,
                "item_category_name": coding_book_data.get(cat_id, {}).get("name"),
                "item_category_description": coding_book_data.get(cat_id, {}).get(
                    "description"
                ),
                "item_phrase_or_tool": skill.get("phrase"),
                "item_justification": None,
            }
            all_rows.append(row)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Consolidation complete. Tidy results saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
