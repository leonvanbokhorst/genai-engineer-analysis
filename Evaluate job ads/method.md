# **Methodology: LLM-Assisted Coding of Job Advertisements for GenAI Engineering**

## 1. Research Goal

The aim is to classify job advertisements into three profiles: **ML Engineer**, **GenAI Engineer**, or **Ambiguous**, using a structured codebook. Rather than having the LLM free-read ads, we treat it as a **structured coder** that extracts features and classifies based on explicit evidence. This ensures reliability, transparency, and comparability with human coding.

---

## 2. Pipeline Overview

The coding process runs in three sequential stages:

### Stage 0 — *Relevance Filtering*

* **Task:** Determine if a job advertisement is relevant to AI/GenAI engineering.
* **Output:** Binary flag (Relevant / Not relevant).
* **Why:** Avoid wasting effort coding irrelevant ads (e.g. marketing or business roles). Keeps dataset focused and noise low.

### Stage 1 — *Feature Extraction*

* **Task:** Identify evidence spans in the job ad and assign codes from the codebook (TASK, TECH, SKILL).
* **Output:** JSON with:

  * Exact text spans (with character offsets or direct quotes).
  * Associated codes (e.g. `TASK3: Modeling`, `TECH3: LLM usage`, `SKILL2: Prompting`).
* **Why:** Creates an **audit trail**. Every code is tied to specific text, preventing hallucinations.
* **Quality benefit:** If human reviewers disagree with the LLM later, they can check exactly which evidence was tagged.

### Stage 2 — *Classification*

* **Task:** Assign the final profile label (ML Engineer, GenAI Engineer, Ambiguous).
* **Input:** *Only* the Stage 1 tags and their evidence quotes.
* **Output:** Single label + rationale referencing the extracted tags.
* **Why tags-only?** Keeps classification grounded in visible evidence. Prevents “context leakage,” where the LLM invents signals outside the codebook. Improves replicability and inter-coder reliability.

---

## 3. Human–Machine Reliability Testing

To establish trust, we run a **calibration phase** before scaling.

1. Select a stratified sample of ~30 job ads (balanced across expected categories).
2. Human coders apply the codebook manually:

   * Stage 0: Relevance.
   * Stage 1: Span tagging.
   * Stage 2: Classification.
3. The LLM runs the same pipeline.
4. Compare results.

### Reliability Metrics

* **Percent Agreement**
  Raw % of times human and LLM give the same label. Easy to interpret, but can be inflated by chance.

* **Cohen’s Kappa (κ)**
  Corrects for chance agreement.

  * κ = 1 → perfect agreement.
  * κ = 0 → agreement no better than chance.
  * Social science convention: κ ≥ .6 = moderate; κ ≥ .8 = substantial.
    We target κ ≥ .6 for the final classification stage.

* **Span-level F1 (Stage 1 only)**
  If you want finer detail: treat extracted spans as units and compute precision/recall vs human spans.

  * **Precision:** % of model-coded spans that were correct.
  * **Recall:** % of human-coded spans that were also found by the model.
  * **F1 = harmonic mean of precision & recall.**

### Why these stats?

* They allow you to pinpoint **where drift happens**:

  * If Stage 0 κ is high but Stage 2 κ is low → classification rules need tuning.
  * If Stage 1 precision is low → the LLM is over-coding features.
  * If Stage 1 recall is low → it’s missing features humans pick up.

---

## 4. Scaling Phase

Once κ ≥ .6 is achieved on calibration:

* Run the pipeline across the full dataset of job ads.
* Export structured JSON for each ad with: relevance flag, tagged spans, final label.

---

## 5. Statistical Analyses

With the coded dataset, you can run both descriptive and inferential statistics:

* **Frequencies / distributions:**

  * % of ads per class (ML Engineer vs GenAI vs Ambiguous).
  * Feature frequencies: how often each TASK, TECH, SKILL appears.

* **Associations:**

  * **Chi-square test (χ²):** test whether features are significantly associated with a class.
    Example: Is `TECH4: RAG` disproportionately common in GenAI Engineer ads?
  * If χ² is significant (p < .05), you can say the feature distribution is *not random*.

* **Co-occurrence analysis:**

  * Which features cluster together in ads? (e.g. TECH3+TASK3 often co-occur in GenAI jobs).

* **Trend analysis:**

  * If you have timestamps, track how proportions shift over time (e.g. GenAI roles increasing post-2023).

---

## 6. Why This Method Works

* **Transparency:** all decisions trace back to explicit evidence spans.
* **Reliability:** κ testing ensures the pipeline aligns with human judgment before scaling.
* **Flexibility:** you can update the codebook, retrain prompts, or swap classifiers without changing the whole pipeline.
* **Auditability:** every ad has a JSON trail from raw text → tags → label.

---

👉 With this setup, you’ve got a **mixed-methods bridge**: qualitative richness (quotes, spans) that you can quantify (frequencies, χ², κ). It’s the kind of rigor that works for both research papers and applied partner reports.

