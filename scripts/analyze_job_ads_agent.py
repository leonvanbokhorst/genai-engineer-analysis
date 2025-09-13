import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import json
from pathlib import Path
import time
import math
from tqdm import tqdm
from typing import List, TypedDict


# --- Schema Definition ---
class JobTask(TypedDict):
    phrase: str
    category: str
    justification: str


class Technology(TypedDict):
    phrase: str
    category: str


class SoftSkill(TypedDict):
    phrase: str
    category: str


class ThematicAnalysis(TypedDict):
    job_tasks: List[JobTask]
    technologies: List[Technology]
    soft_skills: List[SoftSkill]


class ProfileClassification(TypedDict):
    profile: str
    rationale: str


class Analysis(TypedDict):
    profile_classification: ProfileClassification
    thematic_analysis: ThematicAnalysis


# --- Configuration ---
load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file.")

genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
GENERATION_CONFIG = {
    "temperature": 0.2,  # 0.1 = low diversity, 1 = high diversity
    "top_p": 1,  # 1 = no diversity, 0 = full diversity # default is 1
    "top_k": 1,  # 1 = no diversity, 0 = full diversity # default is 1
    "seed": 42,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    "response_schema": Analysis,
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# --- File Paths ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE_DIR / "prompts"
CODING_BOOK_PATH = WORKSPACE_DIR / "CODING_BOOK.md"
INPUT_DATA_PATH = WORKSPACE_DIR / "data" / "consolidated_deduplicated.csv"
OUTPUT_DIR = WORKSPACE_DIR / "data" / "automated_analysis"
FAILED_DIR = OUTPUT_DIR / "failed"

# --- Main Functions ---


def get_analysis_prompt(coding_book, job_description):
    """Creates the prompt for the Gemini API call."""
    return f"""
    **Instructions for the Job Analyst:**

    You are an expert Job Analyst. Your task is to analyze the following job description based on the provided Coding Book and produce a structured JSON output that adheres to the provided schema.

    **Analysis Workflow:**
    1.  **Thematic Analysis:** First, carefully read the job description and the Coding Book. Extract all relevant **and unique** phrases, tools, and skills. For each **Job Task**, you must also provide a brief `justification` explaining why the phrase matches the category.
    2.  **Profile Classification:** After completing the thematic analysis, review your findings. Based on the evidence, assign the single most appropriate job profile from Part 1 of the Coding Book. 
    3.  **Rationale:** Provide a concise rationale explaining your choice of profile, referencing the thematic evidence you found.

    You may change obvious spelling mistakes in the job description, technology names, etc.
    
    ---
    **Coding Book:**

    {coding_book}

    ---
    **Job Description to Analyze:**

    {job_description}
    """


def analyze_job_ad(
    job_ad_text: str, template: str, job_id: int, job_info: dict
) -> dict | None:
    """
    Analyzes a single job ad using the Gemini API.

    Args:
        job_ad_text: The full text of the job advertisement.
        template: The full prompt template including the master prompt and coding book.
        job_id: The unique identifier for the job ad.
        job_info: A dictionary containing all original data for the job ad.

    Returns:
        A dictionary containing the structured analysis from the API, or None on failure.
    """
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
    )

    prompt = template

    try:
        response = model.generate_content(prompt)

        # Clean the response text before parsing
        response_text = response.text
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        analysis_data = json.loads(response_text)

        # Combine original job info with the new analysis
        final_result = {
            "job_id": job_id,
            "job_details": {
                k: (None if isinstance(v, float) and math.isnan(v) else v)
                for k, v in job_info.items()
            },
            "analysis": analysis_data,
        }
        return final_result  # Success
    except Exception as e:
        print(f"An error occurred for job {job_id}: {e}")
        if "response" in locals() and hasattr(response, "text"):
            failed_path = FAILED_DIR / f"failed_job_{job_id}.txt"
            with open(failed_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved failed response to {failed_path}")

        print("Aborting this job.")
        return None


def main():
    """
    Main function to run the analysis pipeline.
    """
    print("--- Starting Automated Job Ad Analysis ---")

    OUTPUT_DIR.mkdir(exist_ok=True)
    FAILED_DIR.mkdir(exist_ok=True)
    print(f"Output directory created/ensured at: {OUTPUT_DIR}")
    print(f"Failed analysis directory created/ensured at: {FAILED_DIR}")

    print("Loading coding book...")
    with open(CODING_BOOK_PATH, "r", encoding="utf-8") as f:
        coding_book = f.read()

    print(f"Loading job data from: {INPUT_DATA_PATH}")
    df = pd.read_csv(INPUT_DATA_PATH)

    df["full_text"] = (
        df["Vacaturetitel"].fillna("") + "\n\n" + df["Functieomschrijving"].fillna("")
    )

    print(f"Found {len(df)} total job ads to analyze.")

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Analyzing Jobs"):
        job_id = row["job_id"]
        job_info = row.to_dict()
        output_path = OUTPUT_DIR / f"analysis_job_{job_id}.json"

        if output_path.exists():
            continue

        job_text = row["full_text"]

        if not job_text.strip():
            print(f"Skipping job {job_id} due to empty text.")
            continue

        print(f"\nAnalyzing job {job_id}: {row['Vacaturetitel'][:50]}...")

        prompt = get_analysis_prompt(coding_book, job_text)

        analysis_result = analyze_job_ad(job_text, prompt, job_id, job_info)

        if analysis_result:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=4)

            print(f"Successfully saved analysis for job {job_id} to {output_path}")
        else:
            print(f"Skipping save for job {job_id} due to repeated failures.")

        time.sleep(0.5)

    print("\n--- Automated Analysis Complete ---")


if __name__ == "__main__":
    main()
