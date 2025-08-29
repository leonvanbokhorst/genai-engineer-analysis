import streamlit as st
import pandas as pd
from pathlib import Path
import json

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
VALIDATION_FILE_PATH = WORKSPACE_DIR / "data" / "validation_sample.csv"
PROFILES = [
    "",  # Default empty value
    "Core GenAI Engineer",
    "Core ML Engineer",
    "AI-Adjacent Software Engineer",
    "Software Engineer",
    "GenAI Specialist",
    "ML Specialist (Data Scientist)",
    "Not Relevant",
]


# --- Helper Functions ---
def load_data():
    """Loads the validation data from the CSV file."""
    try:
        df = pd.read_csv(VALIDATION_FILE_PATH)
        # Ensure validator columns exist and handle potential float conversion of integer scores
        if "validator_profile" not in df.columns:
            df["validator_profile"] = ""
        if "validator_confidence" not in df.columns:
            df["validator_confidence"] = pd.NA
        if "validator_notes" not in df.columns:
            df["validator_notes"] = ""

        # Fill NA for text columns to prevent Streamlit errors
        df["validator_profile"] = df["validator_profile"].fillna("")
        df["validator_notes"] = df["validator_notes"].fillna("")

        return df
    except FileNotFoundError:
        st.error(f"Validation file not found at {VALIDATION_FILE_PATH}")
        return None


def save_data(df):
    """Saves the updated DataFrame back to the CSV."""
    try:
        df.to_csv(VALIDATION_FILE_PATH, index=False, encoding="utf-8")
        return True
    except Exception as e:
        st.error(f"Failed to save data: {e}")
        return False


def display_job_card(job_data):
    """Renders the details of a job ad in a card format."""
    st.subheader(f"Job Title: {job_data['Vacaturetitel']}")
    st.markdown(f"**Job ID:** `{job_data['job_id']}`")

    st.markdown("---")

    # Create three columns for a better layout
    col1, col2, col3 = st.columns([2, 2, 3])

    # --- Column 1: AI Analysis ---
    with col1:
        st.markdown("#### 🤖 My (AI) Analysis")
        st.info(f"**Profile:** {job_data['assigned_profile']}")
        st.warning(f"**My Confidence:** {job_data['confidence_score']}/5")
        with st.expander("See my reasoning"):
            st.markdown(f"> {job_data['profile_rationale']}")

        # --- Extracted Details ---
        st.markdown("---")
        st.markdown("**AI-Extracted Details:**")

        try:
            with st.expander("Tasks"):
                st.json(json.loads(job_data["job_tasks"]))
        except (json.JSONDecodeError, TypeError):
            st.error("Could not parse 'job_tasks' data.")

        try:
            with st.expander("Technologies"):
                st.json(json.loads(job_data["technologies"]))
        except (json.JSONDecodeError, TypeError):
            st.error("Could not parse 'technologies' data.")

        try:
            with st.expander("Soft Skills"):
                st.json(json.loads(job_data["soft_skills"]))
        except (json.JSONDecodeError, TypeError):
            st.error("Could not parse 'soft_skills' data.")

    # --- Column 2: Human Verdict ---
    with col2:
        st.markdown("#### 🧑‍🏫 Your (Human) Verdict")

        current_profile_index = (
            PROFILES.index(job_data["validator_profile"])
            if job_data["validator_profile"] in PROFILES
            else 0
        )
        validator_profile = st.selectbox(
            "Your Profile Assessment:",
            options=PROFILES,
            index=current_profile_index,
            key=f"profile_{job_data['job_id']}",
        )
        validator_confidence = st.slider(
            "Your Confidence (1-5):",
            min_value=1,
            max_value=5,
            value=(
                int(job_data["validator_confidence"])
                if pd.notna(job_data["validator_confidence"])
                else 3
            ),
            key=f"confidence_{job_data['job_id']}",
        )
        validator_notes = st.text_area(
            "Your Notes:",
            value=job_data["validator_notes"],
            key=f"notes_{job_data['job_id']}",
            height=200,
        )

    # --- Column 3: Full Job Description ---
    with col3:
        st.markdown("#### 📄 Original Job Advertisement")
        if pd.notna(job_data["full_text"]) and job_data["full_text"].strip():
            st.text_area("Full Text", job_data["full_text"], height=500)
        else:
            st.error("CRITICAL ERROR: Full job ad text is missing for this record!")

    return validator_profile, validator_confidence, validator_notes


# --- Main App ---
st.set_page_config(layout="wide")
st.title("🧑‍🔬 Job Ad Validation Interface")
st.markdown(
    "Welcome, Master Lonn. Please review my analysis and provide your expert judgment. Your insights are crucial for our mission's success."
)

# Load data and initialize session state
df = load_data()
if df is not None:
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # --- Sidebar for navigation and progress ---
    st.sidebar.title("Navigation")
    st.sidebar.markdown(
        f"Record **{st.session_state.current_index + 1}** of **{len(df)}**"
    )

    # Calculate progress
    validated_count = df["validator_profile"].apply(lambda x: x != "").sum()
    st.sidebar.progress(validated_count / len(df))
    st.sidebar.markdown(f"**{validated_count} / {len(df)}** validated.")

    # Navigation buttons
    if st.sidebar.button("⬅️ Previous") and st.session_state.current_index > 0:
        st.session_state.current_index -= 1

    if st.sidebar.button("Next ➡️") and st.session_state.current_index < len(df) - 1:
        st.session_state.current_index += 1

    st.sidebar.markdown("---")

    # Jump to specific record
    jump_to = st.sidebar.number_input(
        "Jump to record number:",
        min_value=1,
        max_value=len(df),
        value=st.session_state.current_index + 1,
    )
    if jump_to != st.session_state.current_index + 1:
        st.session_state.current_index = jump_to - 1

    # --- Main content area ---
    current_record = df.iloc[st.session_state.current_index]

    # Display the job card and get validator inputs
    v_profile, v_conf, v_notes = display_job_card(current_record)

    # Update the DataFrame with new validation data
    df.loc[st.session_state.current_index, "validator_profile"] = v_profile
    df.loc[st.session_state.current_index, "validator_confidence"] = v_conf
    df.loc[st.session_state.current_index, "validator_notes"] = v_notes

    # Save button
    if st.button("💾 Save My Verdicts", type="primary"):
        if save_data(df):
            st.success("Your verdicts have been saved successfully!")
else:
    st.warning("Could not load data. The application cannot start.")
