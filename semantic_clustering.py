import pandas as pd
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Configuration ---
DATA_FILE = "data/consolidated.csv"
# Using a powerful multilingual model for Dutch and English.
MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
EMBEDDINGS_FILE = (
    f"data/embeddings-{MODEL_NAME.replace('/', '_')}.npy"  # Sanitize filename
)

# --- Core Functions ---


def load_and_prepare_data(file_path):
    """Loads and prepares the job data, returning a clean DataFrame."""
    print(f"Loading data from {file_path}...")
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at {file_path}")
        return None

    df = pd.read_csv(file_path)
    # For consistency, we'll only work with jobs that have a description
    df.dropna(subset=["Functieomschrijving"], inplace=True)
    # Create a unique ID for each job ad to track them
    df["job_id"] = df.index
    print(f"Loaded {len(df)} jobs with descriptions.")
    return df


def generate_embeddings(texts, model_name, cache_file):
    """
    Generates sentence embeddings for a list of texts.
    Caches the embeddings to a file to avoid re-computing on subsequent runs.
    """
    if os.path.exists(cache_file):
        print(f"Loading cached embeddings from {cache_file}...")
        return np.load(cache_file)
    print(f"Generating embeddings using '{model_name}'. This may take a while...")
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Saving embeddings to {cache_file} for future use...")
    np.save(cache_file, embeddings)

    return embeddings


def main():
    """Main function to run the semantic clustering pipeline."""
    df = load_and_prepare_data(DATA_FILE)

    if df is not None:
        # We will use the 'Functieomschrijving' for semantic analysis
        job_descriptions = df["Functieomschrijving"].tolist()

        # Step 1: Generate (or load) embeddings
        embeddings = generate_embeddings(job_descriptions, MODEL_NAME, EMBEDDINGS_FILE)

        print(
            f"Successfully generated/loaded {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}."
        )
        # --- Further steps (clustering, reduction) will be added here ---
        print("Next steps: Clustering and dimensionality reduction.")


if __name__ == "__main__":
    main()
