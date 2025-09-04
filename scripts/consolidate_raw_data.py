import pandas as pd
from pathlib import Path

# --- Configuration ---
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = WORKSPACE_DIR / "data" / "raw"
OUTPUT_CSV = WORKSPACE_DIR / "data" / "consolidated.csv"


def main():
    """
    Finds all .xls files in the input directory, consolidates them into
    a single DataFrame, and saves it as a CSV file.
    """
    print(f"--- Starting Data Consolidation from '{INPUT_DIR}' ---")

    xls_files = list(INPUT_DIR.glob("*.xls"))

    if not xls_files:
        print("No .xls files found. Exiting.")
        return

    print(f"Found {len(xls_files)} .xls files to consolidate.")

    all_dfs = []
    for file in xls_files:
        try:
            # The 'xlrd' engine is required for .xls files.
            df = pd.read_excel(file, engine="xlrd")
            all_dfs.append(df)
            print(f"  - Successfully read {file.name}")
        except Exception as e:
            print(f"  - FAILED to read {file.name}: {e}")

    if not all_dfs:
        print("Could not read any of the .xls files. Exiting.")
        return

    print("Consolidating all dataframes...")
    consolidated_df = pd.concat(all_dfs, ignore_index=True)

    print(f"Total rows consolidated: {len(consolidated_df)}")

    # Ensure the output directory exists
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving consolidated data to '{OUTPUT_CSV}'...")
    consolidated_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("--- Consolidation Complete ---")


if __name__ == "__main__":
    main()
