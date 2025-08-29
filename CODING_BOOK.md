# GenAI Engineer Analysis: Coding Book (v3 - Definitive)

## PART 1: JOB PROFILE CLASSIFICATION

**Primary Goal:** The ultimate goal of the analysis is to assign **one** of the following four profiles to the job advertisement. This classification should be the final conclusion, based on the evidence gathered in Part 2.

### 1. `ML Engineer` (Predictive Modeling Specialist)

- **Definition:** A highly skilled programmer who researches, builds, and designs self-running software to automate predictive models. Their work is fundamentally data-driven, concentrating on algorithms that perform tasks like prediction, classification, time series analysis, anomaly detection and recommendation. MLOps, building and maintaining production-grade systems, is a key part of their work.

- **Core Responsibilities:**

  - Algorithm development and implementation
  - Data preprocessing and feature engineering
  - Model training, evaluation, and statistical validation.
  - Productionizing prototypes from Data Scientists

- **Typical Projects:**

  - Creating a fraud detection system using classifmodels.
  - Developing a customer churn prediction model to reduce attrition.
  - Developing a time series analysis model to predict future sales.

- **Evidence Profile:**

### 2. `GenAI Engineer` (Language, Vision, and Interaction Specialist)

- **Definition:** A software engineer who focuses on designing, developing, fine-tuning, and deploying applications built on top of large language models, diffusion models, and other generative models. They are responsible for building and maintaining production-grade user-facing software systems.

- **Core Responsibilities:**

  - Advanced prompt engineering and optimization
  - Building Retrieval-Augmented Generation (RAG) systems
  - Parameter-Efficient Fine-Tuning (PEFT) of LLMs
  - Developing complex agents with frameworks like LangChain, LangGraph, etc.
  - Building and maintaining production-grade security-aware user-facing software systems.

- **Typical Projects:**

  - Building a customer support chatbot using RAG over internal documents.
  - Fine-tuning an LLM to generate legal or medical documents.
  - Building a chatbot that can interact by voice or text with users about the company's products and services.

- **Evidence Profile:**
  - A strong emphasis on `Modeling (TASK3)` using generative techniques (LLMs, RAG, TTS, Fine-Tuning) and the `Software Development (TASK4)` needed to build applications around them (e.g., using LangChain, Pinecone, FAISS, building security-aware APIs, etc.).

### 4. `Ambiguous / Not Relevant`

- **Definition:** Use this category if the job ad is NOT a technical role, is too vague, too short, business-focused, educational, primarilly focusses on the USE of AI tools to enhance productivity (like AI-powered tools, AI-powered workflows, AI-assisted programming, etc.), or NOT related to AI (like traditional software engineering, media design, traditional infrastructure engineering, marketing, sales, etc.).
- **Evidence Profile:** Lacks significant evidence in the job task categories outlined in Part 2.

---

## PART 2: THEMATIC ANALYSIS CATEGORIES

**Secondary Goal:** To support the final classification, the AI analyst must first perform a thematic analysis, extracting specific phrases and tools from the job ad and categorizing them according to the schema below.

### 2.1 Job Tasks (Inspired by CAIN 2022, Heck et al.)

The analyst will identify phrases in the job description that correspond to the following five task categories.

- **`TASK1: Business Understanding`**: The ability to understand the broader business context, align technical solutions with strategic goals, and translate business needs into technical requirements.
- **`TASK2: Data Engineering`**: The process of designing, building, and maintaining data pipelines and infrastructure. This includes data collection, cleaning, preprocessing, and feature engineering.
- **`TASK3: Modeling`**: The core process of creating, training, or adapting machine learning models. This includes selecting algorithms, model architecture, training, and fine-tuning for specific tasks (both traditional and generative).
- **`TASK4: Software Development`**: Traditional software engineering tasks required to build, integrate, and deploy AI features into user-facing applications. This includes API development, building backend services, and ensuring the application is robust and scalable.
- **`TASK5: Operations Engineering (MLOps)`**: Building and managing the infrastructure and pipelines required to test, deploy, monitor, and maintain ML/GenAI models in production. This is the "DevOps" of the AI world.

### 2.2 Technologies

The analyst will extract the specific name of every tool, library, or platform mentioned and classify it.

- `TECH1: Programming Languages` (e.g., Python, TypeScript, JavaScript, Go, Rust, Java, C++, etc.)
- `TECH2: Cloud Platforms & Services` (e.g., AWS, Azure, GCP, Hugging Face, OpenAI, Anthropic, etc.)
- `TECH3: LLM / Generative Models` (e.g., GPT-4, Llama 3, Claude, Gemini, Mistral, etc.)
- `TECH4: LLM Frameworks & Libraries` (e.g., LangChain, Hugging Face, LangGraph, etc.)
- `TECH5: Vector Stores & Search` (e.g., Pinecone, ChromaDB, FAISS, Weaviate, etc.)
- `TECH6: MLOps & Data Pipelines` (e.g., Airflow, Docker, Kubernetes, etc.)
- `TECH7: Data Visualization` (e.g., Matplotlib, Seaborn, Plotly, etc.)
- `TECH8: Data Processing` (e.g., NumPy, SciPy, etc.)
- `TECH9: Data Storage` (e.g., PostgreSQL, MySQL, MongoDB, etc.)
- `TECH10: Data Modeling` (e.g., PyTorch, TensorFlow, Scikit-learn, etc.)
- `TECH11: Data Analysis` (e.g., Pandas, PySpark, SQL, etc.)

### 2.3 Soft Skills

The analyst will identify phrases related to non-technical, interpersonal skills.

- **`SKILL1: Communication & Collaboration`**: The ability to effectively communicate complex technical concepts to both technical and non-technical audiences.
- **`SKILL2: Learning & Adaptability`**: A demonstrated commitment to continuous learning and the ability to adapt to new technologies, tools, and methodologies in a rapidly evolving field.
- **`SKILL3: Problem Solving & Pragmatism`**: The ability to analyze complex, open-ended problems, apply a blend of creativity and rigor to find solutions, and maintain a practical, results-oriented approach.
- **`SKILL4: Ethical & Legal Responsibility`**: An awareness of and commitment to developing responsible, fair, and transparent AI systems. This includes considering potential biases, privacy implications, and the broader societal impact of the technology.
- **`SKILL5: Innovation & Ownership`**: A proactive and entrepreneurial mindset. The drive to take initiative, lead projects, champion new ideas, and take full responsibility for the quality and success of one's work.

---
