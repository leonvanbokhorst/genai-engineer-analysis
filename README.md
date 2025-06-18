# GenAI Engineer Job Market Analysis: A Semantic Clustering Approach

This project has evolved. We are moving beyond simple keyword analysis to a more sophisticated, scientifically sound method for understanding the job market: **semantic clustering**.

The goal is to automatically discover natural groupings of job descriptions based on their _meaning_, not just the words they contain. This will allow us to answer questions like:

- Do job ads that only mention "AI" cluster together with ads that mention "Generative AI," suggesting they describe the same role?
- What are the distinct _types_ or _flavors_ of GenAI Engineer roles that emerge from the data?
- Can we identify the key skills and technologies that define these emergent clusters?

## Methodology: From Keywords to Meaning

Our new pipeline follows a state-of-the-art Natural Language Processing (NLP) methodology.

### 1. High-Quality Multilingual Embeddings

At the core of this approach is the concept of **text embeddings**. Each job description is fed into a sophisticated deep learning model which outputs a high-dimensional vector (an "embedding"). This vector represents the semantic meaning of the text. Job descriptions with similar meanings will have vectors that are close to each other in this high-dimensional space.

To handle the multilingual nature of our dataset (Dutch and English), we are using the powerful `paraphrase-multilingual-mpnet-base-v2` model from the `sentence-transformers` library. This model is specifically designed to understand and map the meaning of text from over 50 languages into a shared vector space, ensuring high-quality results.

### 2. Caching for Efficiency

Generating embeddings is computationally expensive. To ensure our analysis is fast and repeatable, the pipeline automatically caches the generated embeddings to a file (e.g., `data/embeddings-paraphrase-multilingual-mpnet-base-v2.npy`). On subsequent runs, these embeddings are loaded directly from the cache, saving significant time.

### 3. (Upcoming) Dimensionality Reduction & Clustering

Once we have the embeddings, the next steps in the pipeline will be:

- **Dimensionality Reduction:** Using **UMAP** to reduce the high-dimensional vectors (e.g., 768 dimensions) down to 2 dimensions, which allows for visualization.
- **Clustering:** Using **HDBSCAN**, a powerful density-based algorithm, to identify clusters of job descriptions in the reduced dimensional space. HDBSCAN is effective because it can find clusters of different shapes and sizes, and it can identify which points are "noise" and don't belong to any cluster.

### 4. (Upcoming) Analysis and Visualization

The final step will be to analyze the resulting clusters. We will visualize the clusters on a 2D plot and then programmatically extract the most representative keywords from each cluster to understand its defining theme.

---

## How to Use the Pipeline (Current State)

This pipeline is under construction. The instructions below cover the project up to its current state: generating the embeddings.

### 1. Prerequisites

- Python 3.12+
- `uv` (a fast Python package installer and resolver)

### 2. Setup

**a. Create a Virtual Environment:**

```bash
uv venv -p python3.12
```

**b. Activate the Environment and Install Dependencies:**

```bash
source .venv/bin/activate
uv pip sync pyproject.toml
```

### 3. Run the Embedding Generation

This is the first step of the new pipeline.

```bash
python semantic_clustering.py
```

On the first run, this script will download the multilingual model (approx. 1.1 GB) and generate the embeddings for all job descriptions, caching the result in the `/data` directory. Subsequent runs will be much faster.
