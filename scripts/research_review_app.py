"""Streamlit app for manual review of automated analysis files."""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = WORKSPACE_DIR / "data" / "automated_analysis"
REVIEW_LOG_PATH = WORKSPACE_DIR / "data" / "analysis_review_log.csv"
DEFAULT_SAMPLE_SIZE = 25
RIGOR_OPTIONS = [
    "Not Scientifically Rigorous",
    "Needs Minor Revisions",
    "Scientifically Rigorous",
]


# --- Data Loading Utilities ---
@st.cache_data(show_spinner=False)
def load_analysis_records() -> List[Dict[str, Any]]:
    """Return the parsed automated analysis records."""
    records: List[Dict[str, Any]] = []
    for path in sorted(ANALYSIS_DIR.glob("analysis_job_*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            st.warning(f"Skipping {path.name}: could not parse JSON.")
            continue

        job_details: Dict[str, Any] = payload.get("job_details", {})
        analysis: Dict[str, Any] = payload.get("analysis", {})
        profile_block: Dict[str, Any] = analysis.get("profile_classification", {})
        thematic: Dict[str, Any] = analysis.get("thematic_analysis", {})

        record: Dict[str, Any] = {
            "job_id": payload.get("job_id"),
            "file_name": path.name,
            "file_path": str(path.relative_to(WORKSPACE_DIR)),
            "job_title": job_details.get("Vacaturetitel") or job_details.get("job_title"),
            "employer": job_details.get("Organisatienaam"),
            "location": job_details.get("Standplaats") or job_details.get("Gemeente"),
            "full_text": job_details.get("full_text")
            or job_details.get("Functieomschrijving", ""),
            "profile": profile_block.get("profile", "Unknown"),
            "profile_rationale": profile_block.get("rationale", ""),
            "job_tasks": thematic.get("job_tasks", []),
            "soft_skills": thematic.get("soft_skills", []),
            "technologies": thematic.get("technologies", []),
            "raw_payload": payload,
        }
        records.append(record)

    return records


@st.cache_data(show_spinner=False)
def load_review_log() -> pd.DataFrame:
    """Load existing manual review decisions if they exist."""
    if REVIEW_LOG_PATH.exists():
        try:
            return pd.read_csv(REVIEW_LOG_PATH)
        except Exception as exc:  # pragma: no cover - defensive
            st.warning(f"Could not read existing review log: {exc}")
    return pd.DataFrame(
        columns=[
            "job_id",
            "file_name",
            "reviewer",
            "rigor_assessment",
            "follow_up_required",
            "notes",
            "reviewed_at_utc",
        ]
    )


def save_review_log(new_rows: pd.DataFrame) -> None:
    """Persist updated review log to disk."""
    existing = load_review_log()
    if not existing.empty:
        merged = (
            existing.set_index("job_id")
            .combine_first(new_rows.set_index("job_id"))
            .combine_first(existing.set_index("job_id"))
        )
        merged.update(new_rows.set_index("job_id"))
        merged = merged.reset_index()
    else:
        merged = new_rows
    merged.to_csv(REVIEW_LOG_PATH, index=False, encoding="utf-8")


def render_thematic_section(title: str, items: List[Dict[str, Any]]) -> None:
    """Render job task / technology / soft skill tables."""
    st.markdown(f"**{title}**")
    if not items:
        st.info("No items extracted.")
        return
    df = pd.DataFrame(items)
    st.dataframe(df, use_container_width=True, hide_index=True)


# --- App Layout ---
st.set_page_config(page_title="Automated Analysis Review", layout="wide")
st.title("🔍 Scientific Rigor Review Portal")
st.markdown(
    "This tool draws a random subset of automated analysis files and helps you record "
    "manual scientific rigor assessments."
)

records = load_analysis_records()
if not records:
    st.error(
        "No automated analysis files were found. Ensure the pipeline has produced JSON files "
        "in `data/automated_analysis`."
    )
    st.stop()

all_job_ids = [record["job_id"] for record in records if record.get("job_id") is not None]
review_log = load_review_log()
review_lookup = (
    review_log.set_index("job_id").to_dict(orient="index") if not review_log.empty else {}
)

# --- Sidebar Controls ---
st.sidebar.header("Sampling Controls")

max_sample = max(1, len(all_job_ids))
default_sample_size = min(DEFAULT_SAMPLE_SIZE, max_sample)
sample_size = st.sidebar.slider(
    "Sample size",
    min_value=1,
    max_value=max_sample,
    value=default_sample_size,
)
seed = st.sidebar.number_input("Random seed", value=42, step=1)
reviewer_name = st.sidebar.text_input("Reviewer name", value=st.session_state.get("reviewer", ""))
if reviewer_name:
    st.session_state.reviewer = reviewer_name


def draw_sample() -> List[int]:
    rng = random.Random(int(seed))
    if sample_size >= len(all_job_ids):
        return sorted(all_job_ids)
    return sorted(rng.sample(all_job_ids, sample_size))


if "sample_job_ids" not in st.session_state or st.sidebar.button("🎲 Draw new sample"):
    st.session_state.sample_job_ids = draw_sample()
    st.session_state.sample_drawn_at = datetime.utcnow().isoformat()

sample_job_ids: List[int] = st.session_state.sample_job_ids
sample_records = [rec for rec in records if rec.get("job_id") in sample_job_ids]
sample_records.sort(key=lambda r: sample_job_ids.index(r["job_id"]))

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**Sample contains {len(sample_records)} of {len(records)} available analyses.**"
)
if REVIEW_LOG_PATH.exists():
    st.sidebar.download_button(
        "⬇️ Download review log",
        data=review_log.to_csv(index=False).encode("utf-8"),
        file_name=REVIEW_LOG_PATH.name,
        mime="text/csv",
    )

if reviewer_name:
    st.info(f"Recording reviews under: **{reviewer_name}**")

if "sample_drawn_at" in st.session_state:
    st.caption(
        f"Sample last drawn at {st.session_state.sample_drawn_at} UTC with seed {int(seed)}."
    )

if not sample_records:
    st.warning("No records in current sample. Adjust the sample size or seed and draw again.")
    st.stop()

st.markdown("---")
st.header("Review Queue")

for record in sample_records:
    job_id = record.get("job_id")
    with st.expander(f"Job {job_id} · {record.get('job_title', 'Untitled')}", expanded=False):
        st.markdown(f"**Job ID:** `{job_id}`")
        st.markdown(f"**Source file:** `{record['file_path']}`")

        columns = st.columns([2, 2, 3])
        with columns[0]:
            st.markdown("#### Automated Classification")
            st.markdown(f"**Profile:** {record.get('profile', 'Unknown')}")
            st.markdown("**Rationale:**")
            st.write(record.get("profile_rationale", "No rationale provided."))
        with columns[1]:
            st.markdown("#### Reviewer Assessment")
            existing_review = review_lookup.get(job_id, {})
            default_option = existing_review.get("rigor_assessment", RIGOR_OPTIONS[1])
            if default_option not in RIGOR_OPTIONS:
                default_option = RIGOR_OPTIONS[1]
            rigor_choice = st.radio(
                "Scientific rigor",
                options=RIGOR_OPTIONS,
                index=RIGOR_OPTIONS.index(default_option),
                key=f"rigor_{job_id}",
            )
            follow_up_default = bool(existing_review.get("follow_up_required", False))
            follow_up_required = st.checkbox(
                "Requires follow-up?",
                value=follow_up_default,
                key=f"follow_{job_id}",
            )
            notes_default = existing_review.get("notes", "")
            notes = st.text_area(
                "Reviewer notes",
                value=notes_default,
                key=f"notes_{job_id}",
                height=150,
            )
        with columns[2]:
            st.markdown("#### Job Context")
            st.markdown(f"**Employer:** {record.get('employer', 'Unknown')}")
            st.markdown(f"**Location:** {record.get('location', 'Unknown')}")
            with st.expander("Full job text"):
                st.write(record.get("full_text", "No job text provided."))

        st.markdown("---")
        thematic_cols = st.columns(3)
        with thematic_cols[0]:
            render_thematic_section("Job tasks", record.get("job_tasks", []))
        with thematic_cols[1]:
            render_thematic_section("Technologies", record.get("technologies", []))
        with thematic_cols[2]:
            render_thematic_section("Soft skills", record.get("soft_skills", []))

        with st.expander("Raw analysis payload"):
            st.json(record.get("raw_payload", {}))

st.markdown("---")

if st.button("💾 Save review decisions", type="primary"):
    if not reviewer_name:
        st.error("Please provide a reviewer name in the sidebar before saving.")
    else:
        rows: List[Dict[str, Any]] = []
        timestamp = datetime.utcnow().isoformat()
        for record in sample_records:
            job_id = record.get("job_id")
            rigor = st.session_state.get(f"rigor_{job_id}")
            follow_up = st.session_state.get(f"follow_{job_id}")
            notes_value = st.session_state.get(f"notes_{job_id}", "")
            rows.append(
                {
                    "job_id": job_id,
                    "file_name": record.get("file_name"),
                    "reviewer": reviewer_name,
                    "rigor_assessment": rigor,
                    "follow_up_required": bool(follow_up),
                    "notes": notes_value,
                    "reviewed_at_utc": timestamp,
                }
            )
        save_review_log(pd.DataFrame(rows))
        st.success("Review decisions saved to analysis_review_log.csv")
        st.experimental_rerun()
