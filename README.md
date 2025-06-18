# GenAI Engineer Job Analysis

This project analyzes a dataset of GenAI Engineer and related job descriptions to identify key themes, skills, and technologies in the current job market.

The pipeline performs the following steps:

1.  **Consolidates Data**: Merges multiple `.xls` export files into a single `consolidated.csv`.
2.  **Semantic Clustering**:
    - Generates sentence-transformer embeddings (`paraphrase-multilingual-mpnet-base-v2`) for each job description.
    - Caches embeddings to `embeddings.npy` for faster re-runs.
    - Uses UMAP for dimensionality reduction and HDBSCAN for density-based clustering.
    - Saves the results, including cluster labels and 2D coordinates, to `clustered_jobs.csv`.
3.  **Cluster Visualization**: Creates a 2D scatter plot of the job clusters and saves it as `cluster_visualization.png`.
4.  **Qualitative Analysis**: For each cluster, it performs TF-IDF analysis on the lemmatized text (handling both English and Dutch) to extract and display the most representative keywords, giving insight into the theme of each cluster.

## Setup and Execution

This project uses `uv` for package and environment management.

### The Great Dependency Gauntlet of `uv`

**A Word of Warning:** Our journey through setting up this environment was fraught with peril. We initially used `uv pip sync`, which is extremely strict and **does not** install transitive dependencies (dependencies of dependencies). This led to a long and painful process of adding each missing sub-package manually.

**The Correct Way (The Master Lonn Method):**
The correct way to install the environment is to treat the `pyproject.toml` as a requirements file and let `uv` resolve the entire dependency graph.

1.  **Create the virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  **Install all dependencies using `uv`:**
    ```bash
    uv pip install -r pyproject.toml
    ```
3.  **Download SpaCy Models:**
    The analysis script requires spaCy's language models. Download them with:
    ```bash
    python -m spacy download en_core_web_sm
    python -m spacy download nl_core_news_sm
    ```

### Running the Pipeline

To run the full analysis from start to finish, simply execute the main pipeline script:

```bash
python semantic_clustering.py
```

This will generate the embeddings, perform the clustering, and create the visualization.

To re-run only the final keyword analysis on the existing clustered data:

```bash
python analyze_clusters.py
```

## Analysis Results

The results of the cluster analysis, including the top keywords for each identified cluster, are documented in [`ANALYSIS_RESULTS.md`](./ANALYSIS_RESULTS.md).
