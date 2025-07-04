# GenAI Engineer Coding Book

## Guiding Principles for Analysis

1.  **Semantic, Not Keyword-Based:** The primary instruction for analysis is to use semantic understanding. Classification should be based on how well the text of a job ad aligns with the **Definition** of a category, not on matching specific keywords.
2.  **Multilingual & Mixed-Language Aware:** The analysis must be language-agnostic. The definitions apply to concepts whether they are expressed in English, Dutch, or (most commonly) a mix of Dutch communication with English technical terms.
3.  **Examples are Illustrative:** The `Example Phrases` provided are not a checklist. They are intended to give a flavor of the type of language that might be encountered and to aid in understanding the _intent_ of the category definition.

---

This document provides the definitions for the thematic coding of GenAI Engineer job advertisements. It serves as the single source of truth for both automated (Gemini API) and manual coding to ensure consistency and high inter-rater reliability.

---

## 1. Job Task Categories

### Rationale for a Two-Tiered Categorization

To rigorously test the hypothesis that the GenAI Engineer is fundamentally a software engineering role augmented with AI-specific skills, we are adopting a two-tiered categorization system. This approach differs from the original paper's flat list of categories by explicitly grouping tasks into **Core Software Engineering** and **GenAI Specialization**.

This structure allows us to quantitatively analyze the job market's emphasis. If the "software engineering first" hypothesis is correct, we expect to see a significantly higher frequency of coded phrases within the _Core Software Engineering_ macro-category. This methodological decision enables a more nuanced analysis, directly addressing a central question about the nature of the GenAI Engineer profession.

The following detailed sub-categories provide the necessary granularity for accurate coding, while the two primary macro-categories frame our analysis. `Business Understanding` is kept separate as it represents a general professional skill applicable across senior technical roles.

---

### Macro-Category A: Core Software Engineering

_Encompasses the foundational tasks of building, shipping, and maintaining robust and scalable software applications._

#### 1.A.1. Software Development & Integration

- **Definition:** Traditional software engineering tasks required to build, integrate, and deploy GenAI features into user-facing applications. This includes API development, building backend services, and ensuring the application is robust and scalable.
- **Example Phrases:**
  - "Build a robust API endpoint to serve our new summarization model."
  - "Integrate the GenAI service with our existing web application."

#### 1.A.2. Operations & MLOps (LLMOps)

- **Definition:** Tasks related to the deployment, monitoring, and maintenance of generative models in production. This is the "Ops" in LLMOps/MLOps, focused on automation, scalability, and reliability.
- **Example Phrases:**
  - "Deploy models to a production environment using Kubernetes."
  - "Set up a monitoring system to track model performance and drift."
  - "Create a CI/CD pipeline for automated model retraining and deployment."

---

### Macro-Category B: GenAI Specialization

_Encompasses the unique tasks and skills required to work specifically with generative models and the data that fuels them._

#### 1.B.1. Model Development & Fine-Tuning

- **Definition:** The core activities of creating, training, or adapting generative models. This includes selecting the right base model, fine-tuning on custom data, implementing new model architectures, and quantization/optimization.
- **Example Phrases:**
  - "Fine-tune open-source models like Llama 3 on our internal knowledge base."
  - "Develop and train novel generative model architectures from scratch."
  - "Optimize models for low-latency inference."

#### 1.B.2. Prompt Engineering & RAG

- **Definition:** Tasks focused on designing, testing, and optimizing prompts to elicit desired outputs from generative models. Includes the development and implementation of Retrieval-Augmented Generation (RAG) systems.
- **Example Phrases:**
  - "Design and test complex prompt chains for our agentic workflows."
  - "Develop a RAG pipeline to ground model responses in factual documentation."

#### 1.B.3. Data Engineering & Management

- **Definition:** Tasks related to the collection, storage, cleaning, and processing of data used for training, fine-tuning, or evaluating generative models. This includes building data pipelines and ensuring data quality.
- **Example Phrases:**
  - "Build and maintain data pipelines for fine-tuning our proprietary models."
  - "Manage and curate large-scale datasets for pre-training."
  - "Set up and manage vector stores like Pinecone or Chroma."

---

### Overarching Professional Skills

#### 1.C.1. Business Understanding & Strategy

- **Definition:** Tasks related to understanding business needs, identifying opportunities for GenAI solutions, and aligning projects with company goals. Includes translating business requirements into technical specifications and communicating with non-technical stakeholders.
- **Example Phrases:**
  - "Work with product managers to define the scope of new generative features."
  - "Identify key business problems that can be solved using LLMs."

## 2. Technologies & Tools

The API should extract the specific name of every tool, library, or platform mentioned and classify it into one of the following categories based on its primary function.

---

### Technology Categories & Examples

#### 2.1. Programming Languages

- **Definition:** Core programming languages used for development.
- **Examples:** `Python`, `TypeScript`, `JavaScript`, `Go`, `Rust`, `Java`, `C++`

#### 2.2. Cloud Platforms & Services

- **Definition:** Major cloud providers and their specific AI/ML/Data services.
- **Examples:** `AWS (S3, SageMaker, Bedrock)`, `GCP (Vertex AI, GCS)`, `Azure (OpenAI Service, ML Studio)`, `Hugging Face Hub`

#### 2.3. LLM / Generative Models

- **Definition:** Specific Large Language Models or other types of generative models.
- **Examples:** `GPT-4`, `Claude 3`, `Llama 3`, `Mistral`, `Gemini`, `DALL-E`, `Stable Diffusion`

#### 2.4. LLM Frameworks & Libraries

- **Definition:** Frameworks and libraries designed to build applications on top of LLMs.
- **Examples:** `LangChain`, `LlamaIndex`, `Hugging Face Transformers`, `Haystack`, `Semantic Kernel`

#### 2.5. Vector Databases & Search

- **Definition:** Specialized databases for storing and searching vector embeddings.
- **Examples:** `Pinecone`, `ChromaDB`, `FAISS`, `Weaviate`, `Milvus`, `Elasticsearch (with vector search)`

#### 2.6. MLOps & Data Pipelines

- **Definition:** Tools for building data pipelines, orchestrating workflows, and managing the machine learning lifecycle.
- **Examples:** `Airflow`, `Kubeflow`, `MLFlow`, `Weights & Biases`, `Docker`, `Kubernetes`, `Terraform`

#### 2.7. Traditional Data Tools

- **Definition:** Standard data processing libraries and databases that are not vector-specific.
- **Examples:** `Pandas`, `NumPy`, `PySpark`, `SQL`, `PostgreSQL`, `MongoDB`

---

## 3. Soft Skills

This section defines the non-technical, interpersonal, and mindset-related skills required for the role.

---

### Soft Skill Categories & Examples

#### 3.1. Communication & Collaboration

- **Definition:** The ability to effectively share information with technical and non-technical audiences, and to work productively as part of a team.
- **Example Phrases:**
  - "Clearly communicate complex technical concepts to product managers."
  - "Collaborate with cross-functional teams to deliver on project goals."

#### 3.2. Learning & Adaptability

- **Definition:** A commitment to continuous learning and the ability to adapt quickly in a fast-evolving field. This was the most requested skill in the original paper ("open to learn").
- **Example Phrases:**
  - "A passion for staying on top of the latest research papers and models."
  - "Ability to quickly learn and apply new tools and frameworks."

#### 3.3. Problem Solving & Pragmatism

- **Definition:** The ability to analyze complex problems, think critically, and find effective, practical solutions.
- **Example Phrases:**
  - "Demonstrate a pragmatic approach to solution-building."
  - "Strong analytical and debugging skills."

#### 3.4. Ethical & Legal Responsibility

- **Definition:** A strong awareness of the ethical implications of GenAI, including issues of bias, fairness, transparency, and safety. Includes understanding of the evolving legal and regulatory landscape.
- **Example Phrases:**
  - "A strong commitment to building responsible and ethical AI systems."
  - "Ensure our solutions comply with emerging regulations like the EU AI Act."

#### 3.5. Innovation & Ownership

- **Definition:** A proactive and creative mindset, with the ability to take ownership of projects, drive them forward independently, and propose novel ideas.
- **Example Phrases:**
  - "Take ownership of the end-to-end model development lifecycle."
  - "Proactively identify and explore new and creative applications for GenAI."
