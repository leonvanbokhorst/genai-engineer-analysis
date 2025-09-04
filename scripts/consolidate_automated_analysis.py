import os
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


WORKSPACE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = WORKSPACE_DIR / "data" / "automated_analysis"
OUTPUT_TIDY_CSV = WORKSPACE_DIR / "data" / "automated_analysis_consolidated.csv"
OUTPUT_PROFILES_CSV = WORKSPACE_DIR / "data" / "automated_analysis_profiles.csv"
OUTPUT_PER_JOB_CSV = WORKSPACE_DIR / "data" / "automated_analysis_per_job.csv"


import logging

def parse_job_id(filename: str) -> int:
    """Extract integer job_id from filename like 'analysis_123.json'."""
    stem = Path(filename).stem
    # Expect format analysis_<id>
    try:
        return int(stem.split("_")[1])
    except Exception as e:
        logging.error(f"Failed to parse job_id from filename '{filename}': {e}")
        raise ValueError(f"Invalid filename format for job_id extraction: '{filename}'") from e


def load_json_safely(path: Path) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"WARN: Failed to parse {path.name}: {exc}")
        return {}


def consolidate(input_dir: Path) -> pd.DataFrame:
    """
    Flatten all JSON files into a tidy long-form DataFrame with columns:
    - job_id, category_type, category_id, category_name, phrase, tool_name,
      justification, profile, confidence, rationale
    """
    tidy_rows: List[Dict[str, Any]] = []
    profile_rows: List[Dict[str, Any]] = []
    per_job: Dict[int, Dict[str, Any]] = {}

    files = sorted(input_dir.glob("analysis_*.json"))
    print(f"Found {len(files)} analysis files in {input_dir}")

    for fp in files:
        job_id = parse_job_id(fp.name)
        data = load_json_safely(fp)
        if not data:
            continue

        classification = data.get("classification", {})
        profile = classification.get("profile")
        confidence = classification.get("confidence")
        rationale = classification.get("rationale")

        profile_rows.append(
            {
                "job_id": job_id,
                "profile": profile,
                "confidence": confidence,
                "rationale": rationale,
            }
        )

        # Initialize per-job aggregation structure
        if job_id not in per_job:
            per_job[job_id] = {
                "job_id": job_id,
                "profile": profile,
                "confidence": confidence,
                "rationale": rationale,
                "job_tasks": [],
                "technologies": [],
                "soft_skills": [],
            }

        thematic = data.get("thematic_analysis", {})

        # Job tasks
        for item in thematic.get("job_tasks", []) or []:
            tidy_rows.append(
                {
                    "job_id": job_id,
                    "category_type": "job_task",
                    "category_id": item.get("category_id"),
                    "category_name": item.get("category_name"),
                    "phrase": item.get("phrase"),
                    "tool_name": None,
                    "justification": item.get("justification"),
                }
            )
            per_job[job_id]["job_tasks"].append(item)

        # Technologies
        for item in thematic.get("technologies", []) or []:
            tidy_rows.append(
                {
                    "job_id": job_id,
                    "category_type": "technology",
                    "category_id": item.get("category_id"),
                    "category_name": item.get("category_name"),
                    "phrase": None,
                    "tool_name": item.get("tool_name"),
                    "justification": None,
                }
            )
            per_job[job_id]["technologies"].append(item)

        # Soft skills
        for item in thematic.get("soft_skills", []) or []:
            tidy_rows.append(
                {
                    "job_id": job_id,
                    "category_type": "soft_skill",
                    "category_id": item.get("category_id"),
                    "category_name": item.get("category_name"),
                    "phrase": item.get("phrase"),
                    "tool_name": None,
                    "justification": None,
                }
            )
            per_job[job_id]["soft_skills"].append(item)

    tidy_df = pd.DataFrame(tidy_rows)
    profiles_df = (
        pd.DataFrame(profile_rows).drop_duplicates(subset=["job_id"])
        if profile_rows
        else pd.DataFrame(columns=["job_id", "profile", "confidence", "rationale"])
    )

    per_job_rows: List[Dict[str, Any]] = [
        {
            "job_id": job["job_id"],
            "profile": job["profile"],
            "confidence": job["confidence"],
            "rationale": job["rationale"],
            "job_tasks": json.dumps(job["job_tasks"], ensure_ascii=False),
            "technologies": json.dumps(
                job["technologies"], ensure_ascii=False
            ),
            "soft_skills": json.dumps(job["soft_skills"], ensure_ascii=False),
        }
        for job in per_job.values()
    ]
    per_job_df = pd.DataFrame(per_job_rows)

    # Save outputs
    OUTPUT_TIDY_CSV.parent.mkdir(parents=True, exist_ok=True)
    tidy_df.to_csv(OUTPUT_TIDY_CSV, index=False, encoding="utf-8")
    profiles_df.to_csv(OUTPUT_PROFILES_CSV, index=False, encoding="utf-8")
    per_job_df.to_csv(OUTPUT_PER_JOB_CSV, index=False, encoding="utf-8")

    print(f"Saved tidy dataset to: {OUTPUT_TIDY_CSV}")
    print(f"Saved profiles dataset to: {OUTPUT_PROFILES_CSV}")
    print(f"Saved per-job consolidated dataset to: {OUTPUT_PER_JOB_CSV}")
    return tidy_df


def main():
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input directory does not exist: {INPUT_DIR}")
    consolidate(INPUT_DIR)


if __name__ == "__main__":
    main()
