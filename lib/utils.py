import csv
from typing import Dict, List
import pandas as pd

def interpolate(ts_dict):
    s = pd.Series(ts_dict)
    if len(s) == 0:
        return {}
    s.index = s.index.astype(int)
    y_min = s.index.min()
    y_max = s.index.max()

    s = s.reindex(range(y_min, y_max + 1))
    return s.interpolate().to_dict()


def compare_csv_files(file1_path: str, file2_path: str) -> Dict[str, List[Dict]]:
    """
    Compares two CSV files and returns a dictionary with new, removed and updated rows.

    Args:
        file1_path (str): Path to the first CSV file.
        file2_path (str): Path to the second CSV file.

    Returns:
        Dict[str, List[Dict]]: A dictionary containing the differences between the two files. The dictionary
        has the keys 'new', 'removed', and 'updated', and the values are lists of dictionaries representing the
        rows that have been added, removed, or updated. Each row is represented as a dictionary with column headers
        as keys and row values as values.

    Raises:
        FileNotFoundError: If either of the input files cannot be found.

    """
    # Open the two files and read them as dictionaries
    try:
        with open(file1_path, newline='') as file1, open(file2_path, newline='') as file2:
            reader1 = csv.DictReader(file1)
            reader2 = csv.DictReader(file2)

            # Create dictionaries for each CSV file, with the 'id' column serving as the keys
            rows1 = {row['id']: row for row in reader1}
            rows2 = {row['id']: row for row in reader2}

            # Find the new, removed, and updated rows in the two CSV files
            new_rows = [rows2[id] for id in set(rows2) - set(rows1)]
            removed_rows = [rows1[id] for id in set(rows1) - set(rows2)]
            updated_rows = [(rows1[id], rows2[id]) for id in set(rows2) & set(rows1) if rows1[id] != rows2[id]]

            # Return a dictionary containing the differences between the two CSV files
            return {'new': new_rows, 'removed': removed_rows, 'updated': updated_rows}

    except FileNotFoundError:
        raise FileNotFoundError("One or both of the input files could not be found.")

def convert_values_to_float(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        try:
            output_dict[key] = float(value)
        except ValueError:
            output_dict[key] = value
    return output_dict
