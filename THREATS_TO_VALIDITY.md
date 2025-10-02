# Threats to Validity — Job-Ads Coding with LLMs (tags-only pipeline)

## Internal validity

Your biggest risk is leakage: any moment Stage-2 peeks beyond Stage-1 tags into the raw ad, the label can be justified by untracked context. Keep Stage-2 tags-only with quotes, otherwise you’re correlating with signals you can’t audit. A quieter risk is unitization drift. If Stage-1 extracts long, fuzzy spans, one sentence can “prove” conflicting codes, inflating evidence. Make spans minimal and code-specific, and keep your IoU threshold for span matching explicit (≥.5 works, but report it). Finally, watch prompt drift and model drift. Changing temperature, seed, system prompt, or model version silently shifts decisions. Freeze all run-time parameters and version the prompt, codebook, and model hash; recalibrate whenever any of these change.

## Construct validity

“GenAI Engineer” vs “ML Engineer” is a moving target. Titles are marketing; evidence is verbs. If your codebook doesn’t force concrete behaviors—fine-tune, adapter training, retrieval grounding, eval and serving—your construct collapses into “AI-ish.” Be explicit: RAG must be named, adapters or finetuning must be described, and generic “uses AI tools” stays Ambiguous unless paired with modeling verbs. Boilerplate is adversarial here. Many orgs paste “RAG, LangChain, vector DB” into templates regardless of the actual role. Discount boilerplate unless it co-occurs with a concrete task in the same local span. For signals like “GenAI UX,” decide whether you mean building with foundation models or merely integrating an AI feature; write the negative rule, and enforce it.

## External validity

Your scrape is not the market, it’s a lens on the market. Platforms over-represent certain sectors, seniorities, and geographies; English ads specify tools more than Dutch ads, which can understate modeling work. If Stage-0 relevance filters away on-device or embedded AI roles, you’ll shrink the phenomenon without noticing. Sample across sources and languages, stratify by seniority, and timestamp everything. Rerun calibration on each intake window; the meaning of “GenAI Engineer” in October 2025 isn’t March 2024. Report what your corpus is and isn’t, and avoid claims about the entire job market unless your sampling supports it.

## Conclusion validity

Two pitfalls repeat. First, the κ paradox. With skewed class distributions, raw agreement looks great while κ punishes you; with a bloated “Ambiguous,” κ can collapse even if you’re behaving reasonably. Report both percent agreement and κ, and show per-class metrics so reviewers see where errors live. Second, multiple testing landmines. Chi-square on many features will hand you spurious “significant” associations. Pre-register a small set of hypotheses or adjust p-values; otherwise keep those findings exploratory. Also separate self-agreement (majority vote over five LLM passes) from truth. Self-consistency is a confidence proxy, not a validity claim; the anchor remains human-gold agreement on a held-out set.

## Reliability and procedure

Do a balanced, dated calibration set and keep it blind. Humans should not see model outputs when coding gold, and adjudicators should not see who produced which label. Measure Stage-0 κ on relevance, Stage-1 span-level precision/recall/F1 under a stated IoU rule, and Stage-2 κ on the final label with a confusion matrix. If reliability slips, fix rules, not vibes: tighten disambiguation, add negative examples, and retest. Re-run a mini-calibration whenever you change sources, prompts, models, or codebook.

## Data and metadata risks

Treat titles, locations, and company size as untrusted hints. The body text is evidence; metadata often lies or is stale. When metadata conflicts with body text, flag the record and classify from spans only. De-duplicate templated ads and detect boilerplate paragraphs so they don’t inflate GenAI features across a whole employer.

## Ethics and governance

You’re extracting structure from public ads, but transparency matters. Keep an audit trail per document from raw text to spans to label. Avoid naming individual recruiters in reports, and aggregate when presenting employer-level summaries unless you’ve checked for representativeness. Version your codebook and publish change logs so readers understand why 2025-Q4 labels differ from 2026-Q1.

## Mitigation in one breath

Lock evidence to minimal spans, classify from tags-only, calibrate on a balanced dated set with blind adjudication, report κ plus percent agreement plus span-F1, control multiple testing, discount boilerplate without task verbs, distrust metadata, stratify your sample and rerun calibration on drift, and version everything. Do that, and your inferences stay science, not vibes.
