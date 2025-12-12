#pylint: skip-file
#type: ignore

import os
import json
import argparse
import pandas as pd
from jsonschema import validate, ValidationError

def json_csv(json_path, csv_path, schema_path=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if schema_path:
        with open(schema_path, "r", encoding="UTF-8") as f:
            schema = json.load(f)
        try:
            validate(instance=data, schema=schema)
            print("==> JSON Validated.")
        except:
            print("==> JSON Validation Failed.")
            return

    if isinstance(data, dict) and len(data) == 1:
        key = next(iter(data))
        data = data[key]
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
    parser.add_argument("--schema", required=False, help="Optional JSON schema for validation")

    args = parser.parse_args()

    if args.o is None:
        base = os.path.splitext(os.path.basename(args.i))[0]
        args.o = f"../../data/processed/{base}.csv"
    
    json_csv(args.i, args.o, schema_path=args.schema)

