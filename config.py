# Configuration file for the Job Analysis Pipeline

# Keywords to identify the target job role (e.g., GenAI Engineer)
# These are used to filter the initial dataset.
# The script will search for these in the job title and description.
JOB_FILTER_KEYWORDS = [
    "generative ai",
    "genai",
    "large language model",
    "llm",
    "gpt",
    "dalle",
    "midjourney",
    "stable diffusion",
    "prompt engineer",
    "langchain",
    "llama",
]

# Keywords for Technology Analysis (RQ2)
TECHNOLOGIES = {
    # Programming Languages
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c\\+\\+"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "Go": ["golang", " go "],
    "Rust": ["rust"],
    "SQL": ["sql"],
    # AI/ML/Data Frameworks
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Keras": ["keras"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Hugging Face": ["hugging face", "huggingface"],
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
    "MLFlow": ["mlflow"],
    "Kubeflow": ["kubeflow"],
    # Vector Databases
    "Pinecone": ["pinecone"],
    "Weaviate": ["weaviate"],
    "Milvus": ["milvus"],
    "Chroma": ["chroma"],
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
        "robust",
    ],
}
