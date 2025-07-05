import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
from tqdm import tqdm

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration
INPUT_FILE = "data/consolidated_deduplicated.csv"
OUTPUT_DIR = "data/automated_analysis"
CODING_BOOK_PATH = "CODING_BOOK.md"
MODEL_NAME = os.getenv("GEMINI_MODEL")  # do not change this


def get_coding_book_content(file_path):
    """Reads the content of the coding book."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_analysis_prompt(coding_book, job_description):
    """Creates the prompt for the Gemini API call."""
    return f"""
    **Instructions for the Job Analyst:**

    You are an expert Job Analyst. Your task is to analyze the following job description based on the provided Coding Book and produce a structured JSON output.

    **Analysis Workflow:**
    1.  **Thematic Analysis:** First, carefully read the job description and the Coding Book. Extract all relevant phrases, tools, and skills. For each **Job Task**, you must also provide a brief `justification` explaining why the phrase matches the category.
    2.  **Profile Classification:** After completing the thematic analysis, review your findings. Based on the evidence, assign the single most appropriate job profile from Part 1 of the Coding Book.
    3.  **Confidence Score:** Provide a confidence score (1-5) for your profile classification.
    4.  **Rationale:** Provide a concise rationale (2-3 sentences) explaining your choice of profile, referencing the thematic evidence you found.

    You may change obvious spelling mistakes in the job description, technology names, etc.
    
    **Output Format:**
    Return your analysis as a single, VALID JSON object. **Do not include a "chain of thought" or any other commentary outside of the JSON structure.**

    ```json
    {{
      "thematic_analysis": {{
        "job_tasks": [
          {{
            "category_id": "TASK1",
            "category_name": "<name of the job task category>",
            "phrase": "<extracted phrase>",
            "justification": "<brief justification for the categorization>"
          }}
        ],
        "technologies": [
          {{
            "category_id": "TECH1",
            "tool_name": "<extracted tool>"
          }}
        ],
        "soft_skills": [
          {{
            "category_id": "SKILL1",
            "category_name": "<name of the soft skill category>",
            "phrase": "<extracted phrase>"
          }}
        ]
      }},
      "classification": {{
        "profile": "<chosen profile from Part 1>",
        "confidence": <integer 1-5>,
        "rationale": "<your rationale>"
      }}
    }}
    ```

    ---
    **Coding Book:**

    {coding_book}

    ---
    **Job Description to Analyze:**

    {job_description}
    """


def analyze_job_description(model, prompt):
    """Calls the Gemini API to analyze a job description."""
    try:
        response = model.generate_content(prompt)
        # Assuming the response is a JSON string, we may need to clean it up
        # This is a common source of errors
        cleaned_response = (
            response.text.strip().replace("```json", "").replace("```", "")
        )
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error analyzing job description: {e}")
        return {"profile": "Error", "confidence": 0, "rationale": str(e)}


def main():
    """Main function to run the analysis pipeline."""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read the coding book
    coding_book = get_coding_book_content(CODING_BOOK_PATH)

    # Read the input data
    df = pd.read_csv(INPUT_FILE)

    # Initialize the generative model
    model = genai.GenerativeModel(MODEL_NAME)

    print(f"Starting analysis of {len(df)} job ads...")

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Analyzing Jobs"):
        job_id = index
        job_description = row["Functieomschrijving"]
        output_path = os.path.join(OUTPUT_DIR, f"analysis_{job_id}.json")

        # Skip if already processed
        if os.path.exists(output_path):
            continue

        # Create the prompt
        prompt = get_analysis_prompt(coding_book, job_description)

        # Analyze the job description
        analysis_result = analyze_job_description(model, prompt)

        # Save the result
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=4)

        # To avoid hitting API rate limits
        time.sleep(1)

    print("Analysis complete.")


if __name__ == "__main__":
    main()
