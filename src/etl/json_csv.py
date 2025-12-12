#pylint: skip-file
#type: ignore

import os
import json
import argparse
import pandas as pd

def json_csv(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    
    df = pd.json_normalize(data=data)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)

    print(f"CSV saved to: {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and transform JSON to CSV")
    parser.add_argument("--i", required=True, help="Inp JSON")
    parser.add_argument("--o", required=False, help="Out CSV")

    args = parser.parse_args()

    if args.o is None:
        base = os.path.splitext(os.path.basename(args.i))[0]
        args.o = f"../../data/processed/{base}.csv"
    
    json_csv(args.i, args.o)

