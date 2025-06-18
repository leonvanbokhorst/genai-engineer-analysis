# Configuration file for the Job Analysis Pipeline

# Keywords to identify the target job role (e.g., GenAI Engineer)
# These are used to filter the initial dataset.
# The script will search for these in the job title and description.
JOB_FILTER_KEYWORDS = [
    # Core GenAI Terms
    "generative ai",
    "genai",
    "large language model",
    "llm",
    "gpt",
    "langchain",
    "llama",
    # Foundational AI/ML Concepts
    "natural language processing",
    "nlp",
    "computer vision",
    "semantic search",
    "vector search",
    # Specific Models & Companies
    "claude",
    "anthropic",
    "gemini",
    "mistral",
    # Techniques
    "prompt engineer",
    "fine-tuning",
    "rag",
    "retrieval augmented generation",
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
    "OpenAI": ["openai"],
    "Anthropic": ["anthropic"],
    "Google": ["google"],
    "Meta": ["meta"],
    "Microsoft": ["microsoft"],
    "NVIDIA": ["nvidia"],
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
        "llmops"
        "robust",
    ],
}
