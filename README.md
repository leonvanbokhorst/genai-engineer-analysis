# GenAI Engineer Job Market Analysis

This project provides a flexible pipeline to analyze job market data for specific roles, inspired by the methodology in the paper "What Is an AI Engineer? An Empirical Analysis of Job Ads in The Netherlands" (CAIN 2022). This implementation replays the paper's analysis with a new dataset and a focus on the **Generative AI Engineer** role.

## Findings: The GenAI Engineer Profile (Definitive)

Our final, refined analysis pipeline filtered a dataset of 1,283 job ads down to **1,173 relevant jobs** that mention AI or Generative AI concepts. This comprehensive filter provides a clear and robust profile of the modern AI/GenAI Engineer. The key findings are summarized below.

### Job Tasks (RQ1)

The role is defined by three core pillars: Software Development, GenAI/LLM-specific engineering, and a deep understanding of the business context. This confirms the AI/GenAI Engineer is a product-focused role, not just a research or modeling position.

| Task Category          | Mentions |
| ---------------------- | -------- |
| Software Development   | 991      |
| Business Understanding | 935      |
| GenAI/LLM Engineering  | 753      |
| Modeling               | 647      |
| Operations Engineering | 529      |
| Data Engineering       | 129      |

### Technologies (RQ2)

The technology landscape is dominated by core software engineering tools (Git, Python, Cloud Platforms). Specific AI company ecosystems (OpenAI, Google, Microsoft) are also frequently mentioned, indicating the importance of platform-specific knowledge.

| Technology        | Mentions |
| ----------------- | -------- |
| Git               | 183      |
| Python            | 163      |
| Azure             | 131      |
| AWS               | 129      |
| OpenAI            | 54       |
| ... (and 24 more) | ...      |

### Soft Skills (RQ3)

The ideal candidate is a senior-level figure, expected to be a mentor and an innovator for their team and the company, with a strong emphasis on continuous learning.

| Soft Skill       | Mentions |
| ---------------- | -------- |
| Open to learn    | 519      |
| Coaching         | 512      |
| Innovative       | 487      |
| Team-oriented    | 371      |
| Passionate       | 330      |
| ... (and 5 more) | ...      |

---

## How to Use the Pipeline

This pipeline is designed to be flexible. You can easily adapt it to analyze any job role by changing the keywords in the configuration.

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

### 3. Data Consolidation

**a. Place Data:** Add your source `.xls` files into the `/data` directory.

**b. Run the Consolidation Script:** This script combines all `.xls` files in the `/data` directory into a single `consolidated.csv`.

```bash
python consolidate_data.py
```

### 4. Customize and Run the Analysis

**a. Configure Your Search:**
Open `config.py`. To analyze a different job role, simply change the `JOB_FILTER_KEYWORDS` list. For example, to search for "LLM Engineer":

```python
# in config.py
JOB_FILTER_KEYWORDS = [
    'llm engineer', 'large language model engineer'
    # ... add any other relevant keywords
]
```

You can also customize the keywords for technologies, soft skills, and job tasks in the same file to refine the analysis.

**b. Run the Pipeline:**
Execute the main analysis script. It will use your configuration to filter the jobs and generate a new report.

```bash
python analysis_pipeline.py
```

The results will be printed to your terminal.
