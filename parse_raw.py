import pandas as pd
import json
import argparse
from lib.utils import interpolate
import os

# Set up command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to input CSV file")
args = parser.parse_args()

# Construct output file path based on input file path
file_name =  args.input_file.split("/")[-1].replace(".csv", "")
output_folder = f"data/parsed/{file_name}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df = pd.read_csv(args.input_file, index_col="id")

json_cols = ['carbonAbatement', 'emissions', 'outcome', 'target']

for col in json_cols:
    df[col] = df[col].apply(json.loads)

# Realiserade utsläpp
actual_cols = ['emissions', 'outcome']

# Målbanor
target_cols = ['carbonAbatement', 'target']

# Interpolera målbanor
for col in target_cols:
    df[col] = df[col].apply(interpolate)

def parse_latest_values(ts):
    years = list(ts.keys())
    if len(years) == 0:
        return pd.Series(dtype=float)

    latest_year = max(years)
    return pd.Series({
        "LatestYear": int(latest_year),
        "LatestValue": ts[latest_year],
    })

# Hämta senaste år och värde för observerad data
for col in actual_cols:
    _df = df[col].apply(parse_latest_values).add_prefix(col)
    df = df.join(_df)


def add_latest_target_value(row):
    latest_year = row["outcomeLatestYear"]

    if pd.isna(latest_year):
        return row
    
    try:
        row[f"targetLatestValue"] = row["target"][latest_year]
    except KeyError:
        # Det saknas målvärde för observationsåret
        row[f"targetLatestValue"] = None

    return row

# Lägg till målbanavärde för senaste observerade år
df = df.apply(add_latest_target_value, axis=1)

# Räkna ut diff mellan observerat och mål
df["targetDiff"] = df["outcomeLatestValue"] - df["targetLatestValue"]
df["targetDiffPct"] = (df["outcomeLatestValue"] / df["targetLatestValue"] - 1)
cols = [
    "title", "sector","status","subsector", "co2e",
    "diagramDescription","transitionLabel","transitionUnit",
    "emissionsLatestValue","emissionsLatestYear","modelType",
    "outcomeLatestValue", "outcomeLatestYear","targetLatestValue",
    "targetDiff","targetDiffPct"
]
# Spara
output_file = os.path.join(output_folder, "indicators.csv")
df[cols].to_csv(output_file)
print(f"Write to {output_file}")

#
for col in ["target", "outcome"]:
    _df = df[col].apply(pd.Series)\
        .rename(index=df["diagramDescription"].to_dict())
    
    _df = _df[_df.index.notna() & (_df.index != "empty")]
    output_file = os.path.join(output_folder, f"{col}_by_year.csv")
    _df.to_csv(output_file)
    print(f"Write to {output_file}")

