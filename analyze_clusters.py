import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
from spacy.lang.nl.stop_words import STOP_WORDS as nl_stop
import re

# --- Configuration ---
CLUSTERED_DATA_FILE = "data/clustered_jobs.csv"
NUM_TOP_KEYWORDS = 15  # Number of top keywords to display for each cluster


# --- SpaCy Model Setup ---
def download_spacy_model(model_name):
    """Downloads a spaCy model if it's not already installed."""
    try:
        spacy.load(model_name)
    except OSError:
        print(f"Downloading spaCy model: {model_name}")
        spacy.cli.download(model_name)


# Download necessary models
download_spacy_model("en_core_web_sm")
download_spacy_model("nl_core_news_sm")

# Load models
nlp_en = spacy.load("en_core_web_sm")
nlp_nl = spacy.load("nl_core_news_sm")
final_stop_words = set(en_stop).union(nl_stop)


def lemmatize_text(text):
    """
    Lemmatizes text using spaCy, removing stop words and punctuation.
    It processes text with both English and Dutch models and picks the one
    with more valid (non-stop, non-punct) tokens.
    """
    text = re.sub(r"[^A-Za-z\s]", "", str(text).lower())

    doc_en = nlp_en(text)
    tokens_en = [
        token.lemma_
        for token in doc_en
        if token.is_alpha and token.lemma_ not in final_stop_words
    ]

    doc_nl = nlp_nl(text)
    tokens_nl = [
        token.lemma_
        for token in doc_nl
        if token.is_alpha and token.lemma_ not in final_stop_words
    ]

    # Choose the result with more tokens, assuming it's the better parse
    if len(tokens_en) > len(tokens_nl):
        return " ".join(tokens_en)
    else:
        return " ".join(tokens_nl)


def analyze_clusters(file_path):
    """
    Loads clustered job data and analyzes the text content of each cluster
    to find the most representative keywords using TF-IDF with lemmatization.
    """
    print(f"Loading clustered data from {file_path}...")
    df = pd.read_csv(file_path)

    print("Lemmatizing job descriptions... (This may take a while)")
    df["lemmatized_text"] = df["Functieomschrijving"].apply(lemmatize_text)

    # Get the unique cluster labels, ignoring the noise cluster (-1)
    cluster_labels = sorted([label for label in df["cluster"].unique() if label != -1])

    if not cluster_labels:
        print("No clusters found to analyze (only noise points).")
        return

    print("\n--- Top Keywords per Cluster (Lemmatized) ---")

    for cluster_id in cluster_labels:
        print(f"\n--- Cluster {cluster_id} ---")

        cluster_docs = df[df["cluster"] == cluster_id]["lemmatized_text"].tolist()

        try:
            vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(cluster_docs)

            sum_tfidf = tfidf_matrix.sum(axis=0)

            feature_names = vectorizer.get_feature_names_out()
            sorted_indices = sum_tfidf.A.flatten().argsort()[::-1]

            top_terms = [feature_names[i] for i in sorted_indices[:NUM_TOP_KEYWORDS]]

            print(", ".join(top_terms))

        except ValueError:
            print("Could not analyze cluster (likely too few documents).")


def main():
    """Main function to run the cluster analysis."""
    analyze_clusters(CLUSTERED_DATA_FILE)


if __name__ == "__main__":
    main()
