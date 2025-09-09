import pandas as pd
import os


def deduplicate_csv(input_path, output_path, column_names):
    """
    Reads a CSV file, removes duplicate rows based on a specific column,
    and saves the result to a new CSV file.

    Args:
        input_path (str): The path to the input CSV file.
        output_path (str): The path to save the deduplicated CSV file.
        column_names (str): The name of the column to check for duplicates.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    print(f"Reading data from {input_path}...")
    df = pd.read_csv(input_path)

    print(f"Original number of rows: {len(df)}")

    print(f"Deduplicating data based on the columns: {', '.join(column_names)}...")
    deduplicated_df = df.drop_duplicates(subset=column_names, keep="first")

    print(f"Number of rows after deduplication: {len(deduplicated_df)}")

    num_duplicates = len(df) - len(deduplicated_df)
    print(f"Number of duplicate rows removed: {num_duplicates}")

    # --- Add a unique job_id ---
    print("Adding unique job_id to each row...")
    deduplicated_df = deduplicated_df.reset_index(drop=True)
    deduplicated_df.insert(0, "job_id", deduplicated_df.index)

    # Create the directory for the output file if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Saving deduplicated data to {output_path}...")
    deduplicated_df.to_csv(output_path, index=False)

    print("Deduplication complete.")


if __name__ == "__main__":
    # Define file paths
    # Assuming the script is run from the root of the project
    INPUT_CSV_PATH = os.path.join("data", "consolidated.csv")
    OUTPUT_CSV_PATH = os.path.join("data", "consolidated_deduplicated.csv")
    DEDUPLICATION_COLUMNS = [
        "Organisatienaam",
        "Vacaturetitel",
        "Standplaats",
        "Vacaturelink (origineel)",
        "Beroepsgroep",
        "Beroepsklasse",
        "Beroep",
        "Jaar (van datum gevonden)",
        "Maand (van datum gevonden)",
    ]

    deduplicate_csv(INPUT_CSV_PATH, OUTPUT_CSV_PATH, DEDUPLICATION_COLUMNS)
