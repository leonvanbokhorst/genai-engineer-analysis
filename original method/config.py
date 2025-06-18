# Configuration file for the Job Analysis Pipeline

# Keywords to identify the target job role (e.g., GenAI Engineer)
# This list is sanitized to be more "in the spirit" of the CAIN2022 paper,
# focusing on broad concepts and techniques rather than specific, fast-moving
# product names or libraries.
JOB_FILTER_KEYWORDS = [
    # Foundational AI/ML Terms (often used for GenAI roles)
    "ai",
    "artificial intelligence",
    "machine learning",
    # Core GenAI Concepts
    # "generative ai",
    # "genai",
    # "large language model",
    # "llm",
    # "prompt engineer",
    # "prompt engineering",
    # "prompt",
    # # Foundational AI/ML Concepts (often precursors to GenAI roles)
    # "natural language processing",
    # "nlp",
    # "computer vision",
]

# Keywords for Technology Analysis (RQ2)
TECHNOLOGIES = {
    # Programming Languages
    "Python": ["python"],
    "JavaScript": [r"\bjs\b", "javascript"],
    "TypeScript": [r"\bts\b", "typescript"],
    # AI/ML/Data Frameworks
    "TensorFlow": [r"\btf\b", "tensorflow"],
    "PyTorch": ["torch", "pytorch"],
    "Keras": ["keras"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Hugging Face": ["hugging face", "huggingface", "transformers"],
    "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex"],
    "Spark": ["spark"],
    # Cloud Platforms
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    # DevOps & MLOps
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git"],
    "GitHub / GitLab / Bitbucket": ["github", "git hub", "gitlab", "bitbucket"],
    "MLFlow": ["mlflow"],
    "Kubeflow": ["kubeflow"],
    # Vector Databases
    "Pinecone": ["pinecone"],
    "Weaviate": ["weaviate"],
    "Milvus": ["milvus"],
    "Chroma": ["chroma", "chromadb"],
}

# Keywords for Soft Skills Analysis (RQ3)
SOFT_SKILLS = {
    "Team-oriented": ["team player", "teamwork", "collaborate", "collaboration"],
    "Open to learn": ["learn", "learning", "growth mindset", "curious"],
    "Coaching": ["coach", "mentor", "guide", "train"],
    "Passionate": ["passion", "passionate", "driven"],
    "Result-driven": ["result-driven", "results-oriented", "outcome-focused"],
    "Analytical": ["analytical", "analysis"],
    "Innovative": ["innovative", "creative", "innovation"],
    "Communicative": ["communicate", "communication", "communicator"],
    "Creative": ["creative", "creativity"],
    "Curious": ["curious", "curiosity"],
}

# Keywords for Job Task Analysis (RQ1)
# Based on the 5 categories from the CAIN2022 paper, plus a new one for GenAI
JOB_TASKS = {
    "GenAI/LLM Engineering": [
        "llm",
        "large language model",
        "prompt",
        "fine-tuning",
        "fine tuning",
        "rag",
        "retrieval augmented generation",
        "langchain",
        "llama",
        "transformer",
    ],
    "Software Development": [
        "develop",
        "software engineer",
        "code",
        "api",
        "deploy",
        "maintain",
        "backend",
        "frontend",
    ],
    "Modeling": [
        "model",
        "algorithm",
        "neural network",
        "statistics",
        "research",
        "experiment",
    ],
    "Data Engineering": [
        "data pipeline",
        "data platform",
        "etl",
        "extract transform load",
        "data warehouse",
        "data lake",
    ],
    "Business Understanding": [
        "business",
        "product",
        "stakeholder",
        "requirement",
        "customer",
        "user",
    ],
    "Operations Engineering": [
        "production",
        "monitor",
        "scale",
        "infrastructure",
        "ci/cd",
        "mlops",
        "llmops",
    ],
}
