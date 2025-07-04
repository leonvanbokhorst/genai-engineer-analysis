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

To rigorously test the hypothesis that the GenAI Engineer is fundamentally a software engineering role augmented with AI-specific skills, we are adopting a two-tiered categorization system. This approach differs from the original paper's CAIN2022 (2022 Heck et al.) flat list of categories by explicitly grouping tasks into **Core Software Engineering** and **AI Specialization**.

This structure allows us to quantitatively analyze the job market's emphasis. If the "software engineering first" hypothesis is correct, we expect to see a significantly higher frequency of coded phrases within the _Core Software Engineering_ macro-category. This methodological decision enables a more nuanced analysis, directly addressing a central question about the nature of the GenAI Engineer profession.

The following detailed sub-categories provide the necessary granularity for accurate coding, while the two primary macro-categories frame our analysis. `Business Understanding` is kept separate as it represents a general professional skill applicable across senior technical roles.

---

### Job Profiles

Based on the distribution of tasks between the two macro-categories, each job ad will be assigned one of the following profiles. The distinction between `GenAI` and `ML` engineer is critical.

- **`Core GenAI Engineer`**: A balanced mix of tasks from `Macro-Category A` and `B`. Critically, the tasks and technologies are focused on **Generative AI** (e.g., LLMs, RAG, LangChain, prompt engineering, diffusion models).
- **`Core ML Engineer`**: A balanced mix of tasks from `Macro-Category A` and `B`. The tasks and technologies are focused on **traditional Machine Learning** (e.g., predictive modeling, classification, regression, computer vision) and do not significantly involve generative models.
- **`AI-Adjacent Software Engineer`**: Tasks are predominantly from `Macro-Category A`. The role builds or maintains software that directly uses or supports AI/ML models as a core part of its functionality. The output of their work is an AI-powered feature or system.
- **`Software Engineer`**: Tasks are exclusively from `Macro-Category A`. The role does not involve building or integrating AI models. The job may mention AI-assisted tools for productivity, but the final product is not an AI-powered system.
- **`GenAI Specialist`**: Tasks are predominantly from `Macro-Category B` and are focused on **Generative AI**.
- **`ML Specialist (Data Scientist)`**: Tasks are predominantly from `Macro-Category B` and are focused on **traditional Machine Learning**.
- **`Not Relevant`**: The job ad shows no significant tasks related to either `Core Software Engineering` or `GenAI Specialization`. It is likely an unrelated role (e.g., sales, marketing, traditional data analysis) that may have been caught by broad keyword searches.

### Macro-Category A: Core Software Engineering

_Encompasses the foundational tasks of building, shipping, and maintaining robust and scalable software applications._

#### 1.A.1. Software Development & Integration

- **Definition:** Traditional software engineering tasks required to build, integrate, and deploy GenAI features into user-facing applications. This includes API development, building backend services, and ensuring the application is robust and scalable.
- **Examples:**
  - "Designing, developing, testing, maintaining, and deploying software"
  - "Integrate ML models into deployable Python applications and microservices"
  - "Write production-grade product and platform code"
  - "ensuring that what you deliver is scalable, reliable, and secure"
  - "Je integreert de ontwikkelde machine learning-oplossingen in bestaande systemen en applicaties" (You integrate the developed machine learning solutions into existing systems and applications)
  - "Code review of team members' commits"
  - "je hebt de vrijheid om je creativiteit en technische vaardigheden in te zetten waar het écht telt." (you have the freedom to apply your creativity and technical skills where it really counts.)
  - "Provide technical leadership"
  - "rally peers behind your vision"

#### 1.A.2. Operations & MLOps (LLMOps)

- **Definition:** Building and managing the infrastructure and pipelines required to test, deploy, monitor, and maintain ML/GenAI models and systems in production. This includes CI/CD, versioning, monitoring for drift or performance degradation, and ensuring system uptime and reliability. It is the "DevOps" of the AI world.
- **Examples:**
  - "Build CI/CD pipelines for ML model deployment"
  - "unleashing lightning-fast execution and seamless continuous delivery"
  - "Maintain ML models in production (i.e. retraining, monitoring health and ensuring service availability)"
  - "Collaborate with our AI team to construct an infrastructure that ignites rapid, high-scale deep learning exploration, development, and deployment."
  - "champion of our DevOps culture"
  - "Optimaliseren van onze interne tools en infrastructuur" (Optimizing our internal tools and infrastructure)
  - "Set the standard for observability best practices"

---

### Macro-Category B: GenAI Specialization

_Encompasses the unique tasks and skills required to work specifically with generative models and the data that fuels them._

#### 1.B.1. Model Development & Fine-Tuning

- **Definition:** The core process of creating, training, or adapting machine learning models. This includes selecting appropriate algorithms, defining model architecture, training the model on data, and fine-tuning it for specific tasks. It also encompasses research and experimentation with new modeling techniques.
- **Examples:**
  - "having a strong knowledge of Gen AI alogorithms to using wide variety of AI/ML techniques to solve business problems."
  - "designing the methodology of a wide range of models used in the Trading book."
  - "Develop implementations for Trading Risk methodologies"
  - "Research and choose an appropriate set of potential models and loss functions"
  - "Execute experiments while logging your model's metrics, parameters and metadata to a model registry"
  - "Vervolgens ontwikkel je machine learning-algoritmen en modellen en test je deze om de nauwkeurigheid en robuustheid te waarborgen." (You then develop machine learning algorithms and models and test them to ensure accuracy and robustness.)
  - "Design and implement technical evaluators for LLM assessment."
  - "bouwen van predictive models" (building predictive models)

#### 1.B.2. Prompt Engineering & RAG

- **Definition:** Designing, developing, and refining the prompts used to interact with large language models. This also includes implementing Retrieval-Augmented Generation (RAG) systems, where prompts are dynamically enriched with information retrieved from a knowledge base to improve the relevance and accuracy of the model's responses.
- **Examples:**
  - "De voorwaarden waaraan moet worden voldaan t.a.v. de beslissinguit de bronnen kan worden gehaald." (The conditions that must be met regarding the decision can be extracted from the sources.)
  - "Onderzoek of het functiewaarderingsproces kan worden ondersteund door AI." (Investigate if the job evaluation process can be supported by AI.)
  - "Develop our Community Tools. Kicking this off with our very own AI Chatbot."

#### 1.B.3. Data Engineering & Management

- **Definition:** The process of preparing and managing the data used for training and evaluating models. This includes data collection, cleaning, preprocessing, feature engineering, and creating data pipelines. It also involves managing large datasets and ensuring data quality.
- **Examples:**
  - "formulate the GenAI data architecture"
  - "Perform exploratory data analysis to assess data quality and gain important insights"
  - "Perform feature engineering, be creative and combine new sources with the traditional data warehouses or our vast data lakes"
  - "Develop and manage datasets and evaluation metrics."
  - "optimize dataset management"
  - "Analyse van datasets om inzichten te krijgen" (Analysis of datasets to gain insights)
  - "analyseren van complexe datasets om relevante patronen en trends te identificeren." (analyzing complex datasets to identify relevant patterns and trends.)

---

### Overarching Professional Skills

#### 1.C.1. Business Understanding & Strategy

- **Definition:** The ability to understand the broader business context, align technical solutions with strategic goals, and effectively translate business needs into technical requirements.
- **Examples:**
  - "Design and implement Gen AI use cases for major institutions for their business problems."
  - "develop innovative solutions that meet the needs of our growing user community"
  - "in gesprekken met de klant met de klant begrijp je de projectbehoeften en lever je oplossingen die aan deze behoeften voldoen." (in conversations with the client, you understand the project needs and deliver solutions that meet these needs.)
  - "you will fully immerse yourself in the context of the business in order to come up with the best solution to the challenge."
  - "Be a reliable partner for the business"
  - "Helpen bij de transformatie naar een data-driven organisatie" (Helping with the transformation to a data-driven organization)
  - "Samenwerken met diverse teams om AI en ML oplossingen af te stemmen op bedrijfsdoelen" (Collaborating with various teams to align AI and ML solutions with business goals)

## 2. Technologies & Tools

The API should extract the specific name of every tool, library, or platform mentioned and classify it into one of the following categories based on its primary function.

---

### Technology Categories

_\*\*(No examples needed here as the task is to extract literal tool names)_\*\*

#### 2.1. Programming Languages

- **Definition:** Core programming languages used for development (e.g., `Python`, `Go`).

#### 2.2. Cloud Platforms & Services

- **Definition:** Major cloud providers and their specific AI/ML/Data services (e.g., `AWS SageMaker`, `GCP Vertex AI`, `Azure OpenAI Service`).

#### 2.3. LLM / Generative Models

- **Definition:** Specific Large Language Models or other types of generative models (e.g., `GPT-4`, `Llama 3`, `Claude 3`).

#### 2.4. LLM Frameworks & Libraries

- **Definition:** Frameworks and libraries designed to build applications on top of LLMs (e.g., `LangChain`, `LlamaIndex`, `Hugging Face Transformers`).

#### 2.5. Vector Databases & Search

- **Definition:** Specialized databases for storing and searching vector embeddings (e.g., `Pinecone`, `ChromaDB`, `Weaviate`).

#### 2.6. MLOps & Data Pipelines

- **Definition:** Tools for building data pipelines, orchestrating workflows, and managing the machine learning lifecycle (e.g., `Airflow`, `MLFlow`, `Docker`, `Kubernetes`).

#### 2.7. Traditional Data Tools

- **Definition:** Standard data processing libraries and databases that are not vector-specific (e.g., `Pandas`, `PySpark`, `SQL`).

#### 2.8. Application Frameworks

- **Definition:** Frameworks for building applications, particularly web backends (e.g., `Flutter`, `microservices`).

#### 2.9. Other Technical Skills

- **Definition:** Any other specific technical skill, methodology, or domain-specific tool mentioned (e.g., `RuleSpeak`, `FUWADEF methode`, `3D`).

---

## 3. Soft Skills

This section defines the non-technical, interpersonal, and mindset-related skills required for the role.

---

### Soft Skill Categories & Examples

#### 3.1. Communication & Collaboration

- **Definition:** The ability to work effectively in a team, share knowledge, and communicate complex technical concepts to both technical and non-technical audiences.
- **Examples:**
  - "Good communication & interfacing skills"
  - "Strong in collaboration"
  - "Promote feedback and knowledge sharing culture."
  - "Participate in and lead design reviews with peers and stakeholders."
  - "Contribute to system documentation and team knowledge sharing."
  - "documenteer code, processen en procedures om kennis te behouden en samenwerking te vergemakkelijken." (document code, processes, and procedures to retain knowledge and facilitate collaboration.)
  - "Share your greatest lessons at one of the community events"
  - "Coach junior/medior data scientists & ML Engineers"

#### 3.2. Learning & Adaptability

- **Definition:** A demonstrated commitment to continuous learning and the ability to adapt to new technologies, tools, and methodologies in a rapidly evolving field.
- **Examples:**
  - "Eager to be open to learn, advice & implement new technologies"
  - "comfortable with uncertainty"
  - "Heel veel leergierigheid! Groei is bij ons een must." (A lot of eagerness to learn! Growth is a must for us.)
  - "You are also encouraged and expected to spend 15-20% of your time with us learning new things, doing research and developing yourself."
  - "Onderzoeken van nieuwe technologieen en trends." (Researching new technologies and trends.)
  - "Our biggest expectation is that you'll stay curious. Keep learning. Take on responsibility."

#### 3.3. Problem Solving & Pragmatism

- **Definition:** The ability to analyze complex, open-ended problems, apply a blend of creativity and rigor to find solutions, and maintain a practical, results-oriented approach.
- **Examples:**
  - "showcasing a blend of rigor and creativity when tackling open-ended questions, shaping early ideas, and rigorously testing GenAI solutions."
  - "adopting a practical and pragmatic mindset"

#### 3.4. Ethical & Legal Responsibility

- **Definition:** An awareness of and commitment to developing responsible, fair, and transparent AI systems. This includes considering potential biases, privacy implications, and the broader societal impact of the technology.
- **Examples:**
  - "contributing significantly to the development of impactful and responsible user-centered products and services."
  - "guide responsible innovation"
  - "ensure that every AI feature we deliver is robust, reliable, and meets the highest quality standards."

#### 3.5. Innovation & Ownership

- **Definition:** A proactive and entrepreneurial mindset. The drive to take initiative, lead projects, champion new ideas, and take full responsibility for the quality and success of one's work.
- **Examples:**

  - "showing entrepreneurship"
  - "Take the helm"
  - "Blaze a trail"
  - "champion of our DevOps culture"
  - "lead design reviews"
  - "je hebt de vrijheid om je creativiteit en technische vaardigheden in te zetten waar het écht telt." (you have the freedom to apply your creativity and technical skills where it really counts.)
  - "Provide technical leadership"
  - "rally peers behind your vision"
