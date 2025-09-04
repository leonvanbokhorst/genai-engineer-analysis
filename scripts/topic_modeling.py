import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pathlib import Path
import re
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
from spacy.lang.nl.stop_words import STOP_WORDS as nl_stop

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
INPUT_DATA_CSV = WORKSPACE_DIR / "data" / "consolidated_deduplicated.csv"
OUTPUT_DIR = WORKSPACE_DIR / "data" / "analysis_results"
NUM_TOPICS = 10
TOP_WORDS_PER_TOPIC = 15

# --- SpaCy setup ---
# Load the spaCy model. Ensure you have downloaded it:
# python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    exit()

# Combine English and Dutch stop words for more robust filtering
custom_stopwords = en_stop.union(nl_stop)


def preprocess_text(text):
    """
    Cleans and prepares text for topic modeling using spaCy.
    - Removes punctuation and numbers
    - Converts to lowercase
    - Lemmatizes
    - Removes a combined list of English and Dutch stop words
    """
    if not isinstance(text, str):
        return ""

    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub(r"[^a-zA-Z\s]", "", text, re.I | re.A).lower().strip()

    doc = nlp(text)

    # Lemmatize and remove stop words
    tokens = [
        token.lemma_
        for token in doc
        if token.text not in custom_stopwords
        and token.is_alpha
        and len(token.lemma_) > 2
    ]

    return " ".join(tokens)


def display_topics(model, feature_names, no_top_words):
    """Prints the top words for each topic."""
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        top_words = " | ".join(
            [feature_names[i] for i in topic.argsort()[: -no_top_words - 1 : -1]]
        )
        print(f"Topic {topic_idx}: {top_words}")
        topic_dict[topic_idx] = top_words
    return topic_dict


def main():
    """
    Main function to run the topic modeling pipeline.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading data...")
    df = pd.read_csv(INPUT_DATA_CSV)

    # Combine relevant text fields for a comprehensive analysis
    df["full_text"] = (
        df["Vacaturetitel"].fillna("") + " " + df["Functieomschrijving"].fillna("")
    )

    print("Preprocessing text data... (this may take a few minutes)")
    df["processed_text"] = df["full_text"].apply(preprocess_text)

    # Filter out any empty documents that might result from preprocessing
    processed_docs = df["processed_text"][df["processed_text"].str.len() > 0]

    print("Vectorizing text with TF-IDF...")
    # We use TF-IDF to give higher weight to words that are more unique to a document
    vectorizer = TfidfVectorizer(max_df=0.9, min_df=25)
    tfidf_matrix = vectorizer.fit_transform(processed_docs)

    print(f"Running Latent Dirichlet Allocation (LDA) for {NUM_TOPICS} topics...")
    lda = LatentDirichletAllocation(n_components=NUM_TOPICS, random_state=42)
    lda.fit(tfidf_matrix)

    print("\n--- Discovered Topics ---")
    feature_names = vectorizer.get_feature_names_out()
    topics = display_topics(lda, feature_names, TOP_WORDS_PER_TOPIC)

    # --- Assign dominant topic to each document ---
    print("\nAssigning dominant topic to each job ad...")
    doc_topic_dist = lda.transform(tfidf_matrix)
    dominant_topic = np.argmax(doc_topic_dist, axis=1)

    # Create a DataFrame with job_id and the assigned topic
    # We need to align it with the original DataFrame's index
    df_topics = pd.DataFrame(
        {"job_id": processed_docs.index, "dominant_topic": dominant_topic}
    )

    output_topic_mapping_path = OUTPUT_DIR / "job_topic_mapping.csv"
    df_topics.to_csv(output_topic_mapping_path, index=False)
    print(f"Saved job-to-topic mapping to {output_topic_mapping_path}")

    # Save topic definitions to a file
    df_topic_defs = pd.DataFrame.from_dict(
        topics, orient="index", columns=["top_words"]
    )
    df_topic_defs.index.name = "topic_id"
    output_topic_defs_path = OUTPUT_DIR / "topic_definitions.csv"
    df_topic_defs.to_csv(output_topic_defs_path)
    print(f"Saved topic definitions to {output_topic_defs_path}")

    # Save results to a text file
    output_path = OUTPUT_DIR / "topic_modeling_results.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Topic Modeling Results ({NUM_TOPICS} topics)\n")
        f.write("=" * 40 + "\n")
        for topic_id, words in topics.items():
            f.write(f"Topic {topic_id}: {words}\n")

    print(f"\nSaved topic modeling results to {output_path}")


if __name__ == "__main__":
    main()
