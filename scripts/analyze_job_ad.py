import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import json
from pathlib import Path
import time
from tqdm import tqdm

# --- Configuration ---
load_dotenv()  # Load variables from .env file

# Add your Google API Key to your environment variables or a .env file
# For example, in your ~/.zshrc or ~/.bashrc add:
# export GOOGLE_API_KEY='YOUR_API_KEY'
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file.")

genai.configure(api_key=API_KEY) # type: ignore

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
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
MASTER_PROMPT_PATH = PROMPTS_DIR / "master_prompt.md"
INPUT_DATA_PATH = WORKSPACE_DIR / "data" / "consolidated.csv"
OUTPUT_DIR = WORKSPACE_DIR / "data" / "automated_analysis"

# --- Main Functions ---


def load_prompt_template():
    """Loads the master prompt and the coding book."""
    with open(CODING_BOOK_PATH, "r", encoding="utf-8") as f:
        coding_book = f.read()
    with open(MASTER_PROMPT_PATH, "r", encoding="utf-8") as f:
        master_prompt = f.read()

    return f"{master_prompt}\n\n---\n\n## CODING_BOOK.md\n\n{coding_book}"


def analyze_job_ad(job_ad_text: str, template: str) -> dict:
    """
    Analyzes a single job ad using the Gemini API.

    Args:
        job_ad_text: The full text of the job advertisement.
        template: The full prompt template including the master prompt and coding book.

    Returns:
        A dictionary containing the structured analysis from the API.
    """
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
    )

    prompt = f"{template}\n\n---\n\n## Job Advertisement to Analyze:\n\n```text\n{job_ad_text}\n```"

    try:
        response = model.generate_content(prompt)
        # The API is configured to return JSON directly, so we parse the text part.
        return json.loads(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        # In case of an error, we still want to see the raw response if possible
        if "response" in locals() and hasattr(response, "prompt_feedback"):
            print(f"Prompt Feedback: {response.prompt_feedback}")
        return {"error": str(e)}


def main():
    """
    Main function to run the analysis pipeline.
    """
    print("--- Starting Automated Job Ad Analysis ---")

    # 1. Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"Output directory created/ensured at: {OUTPUT_DIR}")

    # 2. Load the prompt template
    print("Loading prompt template and coding book...")
    prompt_template = load_prompt_template()

    # 3. Load the input data
    print(f"Loading job data from: {INPUT_DATA_PATH}")
    df = pd.read_csv(INPUT_DATA_PATH)

    # For the purpose of this script, we'll combine relevant text fields
    df["full_text"] = (
        df["Vacaturetitel"].fillna("") + "\n\n" + df["Functieomschrijving"].fillna("")
    )

    print(f"Found {len(df)} total job ads to analyze.")

    # --- Analysis Loop ---
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Analyzing Jobs"):
        job_id = index
        output_path = OUTPUT_DIR / f"analysis_job_{job_id}.json"

        # Skip if already analyzed
        if output_path.exists():
            continue

        job_text = row["full_text"]

        # Simple check to skip empty job ads
        if not job_text.strip():
            print(f"Skipping job {job_id} due to empty text.")
            continue

        print(f"\nAnalyzing job {job_id}: {row['Vacaturetitel'][:50]}...")

        analysis_result = analyze_job_ad(job_text, prompt_template)

        # Save the result
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=4)

        print(f"Successfully saved analysis for job {job_id} to {output_path}")

        # Rate limiting: be respectful to the API
        time.sleep(2)  # 30 requests per minute

    print("\n--- Automated Analysis Complete ---")


if __name__ == "__main__":
    main()
