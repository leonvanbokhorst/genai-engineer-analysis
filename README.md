# GenAI Engineer Job Market Analysis: A Semantic Clustering Approach

This project has evolved. We are moving beyond simple keyword analysis to a more sophisticated, scientifically sound method for understanding the job market: **semantic clustering**.

The goal is to automatically discover natural groupings of job descriptions based on their _meaning_, not just the words they contain. This allows us to answer questions like:

- Do job ads that only mention "AI" cluster together with ads that mention "Generative AI," suggesting they describe the same role?
- What are the distinct _types_ or _flavors_ of GenAI Engineer roles that emerge from the data?
- Can we identify the key skills and technologies that define these emergent clusters?

## Methodology: From Keywords to Meaning

Our new pipeline follows a state-of-the-art Natural Language Processing (NLP) methodology.

### 1. High-Quality Multilingual Embeddings

At the core of this approach is the concept of **text embeddings**. Each job description is fed into a sophisticated deep learning model which outputs a high-dimensional vector (an "embedding"). This vector represents the semantic meaning of the text. Job descriptions with similar meanings will have vectors that are close to each other in this high-dimensional space.

To handle the multilingual nature of our dataset (Dutch and English), we are using the powerful `paraphrase-multilingual-mpnet-base-v2` model from the `sentence-transformers` library. This model is specifically designed to understand and map the meaning of text from over 50 languages into a shared vector space, ensuring high-quality results.

### 2. Caching for Efficiency

Generating embeddings is computationally expensive. To ensure our analysis is fast and repeatable, the pipeline automatically caches the generated embeddings to a file (`data/embeddings-paraphrase-multilingual-mpnet-base-v2.npy`). On subsequent runs, these embeddings are loaded directly from the cache, saving significant time.

### 3. Dimensionality Reduction & Clustering

Once we have the embeddings, the pipeline performs two crucial steps:

- **Dimensionality Reduction:** Using **UMAP** to reduce the high-dimensional vectors (768 dimensions) down to 2 dimensions for visualization and more effective clustering.
- **Clustering:** Using **HDBSCAN**, a powerful density-based algorithm, to identify clusters of job descriptions in the reduced dimensional space. HDBSCAN is effective because it can find clusters of different shapes and sizes, and it can identify which points are "noise" and don't belong to any cluster.

The result of this process is a new file, `data/clustered_jobs.csv`, which contains the original job data enriched with cluster labels and 2D coordinates for visualization.

### 4. (Upcoming) Analysis and Visualization

The next logical step is to analyze and visualize the resulting clusters. This will involve creating a new script to:

- Create a 2D scatter plot of the clusters.
- Programmatically extract the most representative keywords from each cluster to understand its defining theme.
- Interactively explore the clusters to gain insights into the different types of GenAI Engineer roles.

---

## How to Use the Pipeline

### 1. Prerequisites

- Python 3.12+
- `uv` (a fast Python package installer and resolver)

### 2. Setup & The Dependency Gauntlet

**a. Create a Virtual Environment:**

```bash
uv venv -p python3.12
```

**b. A Note on Dependencies:**

Our journey to a working environment was fraught with peril. The `uv pip sync` command, while fast, is extremely strict and **does not install transitive dependencies** (dependencies of your dependencies). This led to a long and arduous process of identifying and manually adding every single required package to our `pyproject.toml`.

To save you from this trial by fire, ensure your `pyproject.toml`'s `[project]` section includes the following complete list of dependencies:

```toml
dependencies = [
    "pandas",
    "openpyxl",
    "xlrd",
    "numpy<=2.2",
    "pytz",
    "python-dateutil",
    "six",
    "pymupdf",
    "sentence-transformers",
    "scikit-learn",
    "umap-learn",
    "hdbscan",
    "matplotlib",
    "seaborn",
    "huggingface-hub",
    "requests",
    "urllib3",
    "idna",
    "chardet",
    "certifi",
    "transformers",
    "tqdm",
    "torch",
    "scipy",
    "Pillow",
    "typing_extensions",
    "pyyaml",
    "filelock",
    "packaging",
    "regex",
    "safetensors",
    "tokenizers",
    "joblib",
    "threadpoolctl",
    "sympy",
    "mpmath",
    "numba",
    "llvmlite",
    "pynndescent",
    "pyparsing",
    "cycler",
    "kiwisolver",
]
```

**c. Activate the Environment and Install Dependencies:**

```bash
source .venv/bin/activate
uv pip sync pyproject.toml
```

### 3. Run the Analysis Pipeline

The project now contains two main scripts:

**a. Run the Clustering Pipeline:**

This command will run the entire pipeline: loading data, generating/loading embeddings, reducing dimensionality, and performing clustering.

```bash
python semantic_clustering.py
```

This will produce the `data/clustered_jobs.csv` file.

**b. Run the Visualization Script:**

Once the clustering is complete, you can generate a visualization of the clusters.

```bash
python visualize_clusters.py
```

This will create the `data/cluster_visualization.png` image file.

## Next Steps

With the clusters identified and visualized, the next logical step is to perform a qualitative analysis to understand the _meaning_ of each cluster. This involves creating a new analysis script to:

- Load the `clustered_jobs.csv` data.
- For each cluster, extract the most common words or n-grams from the `Functieomschrijving` (job description) to identify its theme.
- Present a summary of each cluster's defining characteristics.
