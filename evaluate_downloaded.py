import argparse
import os
from lib.utils import compare_csv_files
import shutil

# Set path to latest.csv
LATEST_CSV = "data/raw/latest.csv"

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input CSV file")
    args = parser.parse_args()


    # Check if latest.csv exists
    if os.path.exists(LATEST_CSV):
        # Compare input file to latest.csv
        changes = compare_csv_files(args.input_file, LATEST_CSV)

        # If files differ, overwrite latest.csv with input file and store a copy to data/raw
        if any(changes.values()):
            shutil.copy(args.input_file, LATEST_CSV)
            shutil.copy(LATEST_CSV, f"data/raw/{os.path.basename(args.input_file)}")
            print(f"{args.input_file} has been stored as {LATEST_CSV}, and a copy has been saved to data/raw.")
        else:
            print("No changes found, latest.csv was not updated.")

    else:
        # Store input file as latest.csv
        os.rename(args.input_file, LATEST_CSV)
        print(f"{args.input_file} has been stored as {LATEST_CSV}.")
        shutil.copy(LATEST_CSV, f"data/raw/{os.path.basename(args.input_file)}")

if __name__ == "__main__":
    main()
