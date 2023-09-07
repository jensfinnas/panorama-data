import requests
import pandas as pd 
from datetime import datetime
import json
import os

OUTDIR = "tmp"
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

today = datetime.now().strftime('%Y-%m-%d')
outfile_json = os.path.join(OUTDIR, f"{today}.json")
outfile_csv = os.path.join(OUTDIR, f"{today}.csv")

# Scrape
url = "https://api.climateview.net/boards/Boards/ec2d0cdf-e70e-43fb-85cb-ed6b31ee1e09/published/v3"
print(f"/GET {url}")
r = requests.get(url, verify=False)


# Store a copy of the raw file
json_data = r.json()

with open(outfile_json, "w") as f:
    json.dump(json_data, f, indent=2)
    print(f"=> {outfile_json}")

# Parse key data and store to csv file
def get_values(d):
    """Parse non-nested values (no dicts or lists)"""
    values = {}
    for k, v in d.items():
        if isinstance(v, list) or isinstance(v, dict):
            continue
        values[k] = v
    return values


nodes = []
for node_id, node_data in json_data["content"]["entityData"]["nodes"].items():
    node = {
        "id": node_id,
        "title": node_data["title"],
    }
    # parse data
    node.update(get_values(node_data["nodeProperties"]))

    if "customTargetModelData" in node_data["nodeProperties"]:
        # parse more data
        node.update(get_values(node_data["nodeProperties"]["customTargetModelData"]))
        
        # get timeserie data from charts
        chart_data = node_data["nodeProperties"]["customTargetModelData"]["chartData"]
        for k, v in chart_data.items():
            node[k] = json.dumps(v)
        
        nodes.append(node)

df_nodes = pd.DataFrame(nodes).set_index("id")
df_nodes.to_csv(outfile_csv)
print(f"=> {outfile_csv}")

