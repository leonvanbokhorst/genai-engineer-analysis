MOCK UP of results. Numbers are fake but realistic for a 30-ad calibration.

**Calibration sample (n=30)**

| Class (human gold) | Count |
| ------------------ | ----: |
| ML Engineer        |    10 |
| GenAI Engineer     |    10 |
| Ambiguous          |    10 |

**Stage 0 — Relevance filter (binary)**

| Metric            | Value |
| ----------------- | ----: |
| Percent agreement |  0.93 |
| Cohen’s κ         |  0.86 |

**Stage 1 — Feature extraction (span-level)**

| Metric (micro-avg over all codes) |                                                                 Value |
| --------------------------------- | --------------------------------------------------------------------: |
| Precision                         |                                                                  0.78 |
| Recall                            |                                                                  0.72 |
| F1                                |                                                                  0.75 |
| Notes                             | Span = exact quoted evidence; match if overlaps ≥50% and code matches |

**Stage 2 — Final classification (tags-only input)**

| Metric            | Value |
| ----------------- | ----: |
| Percent agreement |  0.83 |
| Cohen’s κ         |  0.74 |

**Stage 2 confusion matrix (rows = human, cols = LLM)**

|              | ML Eng | GenAI Eng | Ambiguous | Row total |
| ------------ | -----: | --------: | --------: | --------: |
| ML Eng       |      8 |         1 |         1 |        10 |
| GenAI Eng    |      1 |         7 |         2 |        10 |
| Ambiguous    |      0 |         2 |         8 |        10 |
| Column total |      9 |        10 |        11 |        30 |

Kort lezen: filter is solide (κ=.86), tagging is “goed genoeg” voor schaal (F1=.75), en de eindlabeler zit in “substantial-ish” territory (κ=.74). De fouten zitten vooral op de grens ML↔GenAI en GenAI↔Ambiguous—precies waar je het verwacht.

