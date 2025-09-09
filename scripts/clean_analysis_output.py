import pandas as pd
import re
import argparse
from pathlib import Path


def clean_consolidated_file(input_file: Path, output_file: Path):
    """
    Cleans the category_name column in the consolidated CSV file.
    This is a more robust version that handles multiple patterns.
    """
    if not input_file.exists():
        print(f"Error: Consolidated input file not found at {input_file}")
        return

    print(f"Reading consolidated data from {input_file}...")
    df = pd.read_csv(input_file)

    # Ensure category_name is workable
    names = df["category_name"].astype(str).copy()

    # 1. Strip prefixes like 'TASK1: ', 'SKILL2: ', etc.
    names = names.str.replace(r"^[A-Z]+\d*:\s*", "", regex=True)

    # 2. Nullify entries that are just prefixes like 'TASK1', 'TECH', 'SKILL2'
    # This is more robust and case-insensitive.
    names = names.str.replace(
        r"^(TASK|SKILL|TECH)\d*$", "", regex=True, flags=re.IGNORECASE
    )

    # 3. Strip any leading/trailing whitespace
    names = names.str.strip()

    # 4. Replace empty strings with NA so they are treated as nulls
    names.replace("", pd.NA, inplace=True)

    # 5. Handle specific known messy values if any
    names.replace(
        "Communication & Communication", "Communication & Collaboration", inplace=True
    )

    df["category_name"] = names
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Cleaned consolidated data saved to {output_file}")


def clean_profiles_file(input_file: Path, output_file: Path):
    """
    Cleans the profile column in the profiles CSV file.
    Removes backticks and standardizes whitespace.
    """
    if not input_file.exists():
        print(f"Error: Profiles input file not found at {input_file}")
        return

    print(f"Reading profiles data from {input_file}...")
    df = pd.read_csv(input_file)

    profiles = df["profile"].astype(str).copy()

    # Remove backticks
    profiles = profiles.str.replace("`", "", regex=False)

    # Standardize whitespace
    profiles = profiles.str.strip()

    df["profile"] = profiles
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Cleaned profiles data saved to {output_file}")


def main():
    """Main function to run the cleaning scripts."""
    parser = argparse.ArgumentParser(
        description="Clean the consolidated analysis and profiles CSV files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    workspace_dir = Path(__file__).resolve().parent.parent
    default_consolidated = (
        workspace_dir / "data" / "automated_analysis_consolidated.csv"
    )
    default_profiles = workspace_dir / "data" / "automated_analysis_profiles.csv"

    parser.add_argument(
        "--consolidated-file",
        type=Path,
        default=default_consolidated,
        help="Path to the consolidated CSV file.",
    )
    parser.add_argument(
        "--profiles-file",
        type=Path,
        default=default_profiles,
        help="Path to the profiles CSV file.",
    )

    args = parser.parse_args()

    clean_consolidated_file(args.consolidated_file, args.consolidated_file)
    clean_profiles_file(args.profiles_file, args.profiles_file)


if __name__ == "__main__":
    main()
