import pandas as pd
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from umap import UMAP
import hdbscan
from sklearn.metrics import pairwise_distances

# --- Configuration ---
DATA_FILE = "data/consolidated.csv"
# Using a powerful multilingual model for Dutch and English.
MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
EMBEDDINGS_FILE = (
    f"data/embeddings-{MODEL_NAME.replace('/', '_')}.npy"  # Sanitize filename
)
CLUSTERED_DATA_FILE = "data/clustered_jobs.csv"

# --- Clustering Parameters ---
N_NEIGHBORS = 15
MIN_DIST = 0.1
MIN_CLUSTER_SIZE = 20  # A more balanced setting
METRIC = "cosine"

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


def reduce_dimensionality(embeddings):
    """
    Reduces the dimensionality of embeddings using UMAP.
    """
    print("Reducing dimensionality with UMAP...")
    reducer = UMAP(
        n_neighbors=N_NEIGHBORS, min_dist=MIN_DIST, metric=METRIC, random_state=42
    )
    reduced_embeddings = reducer.fit_transform(embeddings)
    print(f"Dimensionality reduced to {reduced_embeddings.shape}.")
    return reduced_embeddings


def perform_clustering(embeddings, df):
    """
    Performs clustering using HDBSCAN and returns the updated DataFrame.
    """
    print("Clustering with HDBSCAN...")
    # HDBSCAN works well with precomputed distances
    distance_matrix = pairwise_distances(embeddings, metric=METRIC)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=MIN_CLUSTER_SIZE,
        metric="precomputed",
        cluster_selection_epsilon=CLUSTER_SELECTION_EPSILON,
    ).fit(
        distance_matrix.astype(np.float64)
    )  # Ensure float64 dtype

    # Add cluster labels to the DataFrame
    df["cluster"] = clusterer.labels_

    num_clusters = len(set(clusterer.labels_)) - (1 if -1 in clusterer.labels_ else 0)
    num_noise = list(clusterer.labels_).count(-1)

    print(f"Found {num_clusters} clusters and {num_noise} noise points.")
    return df


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

        # Step 2: Reduce dimensionality for visualization and easier clustering
        reduced_embeddings = reduce_dimensionality(embeddings)
        df["x"] = reduced_embeddings[:, 0]
        df["y"] = reduced_embeddings[:, 1]

        # Step 3: Perform clustering on the original high-dimensional embeddings
        df_clustered = perform_clustering(embeddings, df)

        # Step 4: Save the results
        print(f"Saving clustered data to {CLUSTERED_DATA_FILE}...")
        df_clustered.to_csv(CLUSTERED_DATA_FILE, index=False)
        print("Done.")


if __name__ == "__main__":
    main()
