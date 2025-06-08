#!/usr/bin/env python3

import os
import glob
import pandas as pd

# Paths
raw_dir = "data/raw"
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

# File pattern
csv_files = sorted(glob.glob(os.path.join(raw_dir, "on_time_performance_2023_*.csv")))
print(f"Found {len(csv_files)} CSV files.")

# Correct column names from BTS file
columns_to_keep = [
    "FLIGHTDATE", "REPORTING_AIRLINE", "TAIL_NUMBER",
    "ORIGIN", "DEST",
    "DEPDELAY", "ARRDELAY", "CANCELLED", "CANCELLATIONCODE",
    "WEATHERDELAY", "NASDELAY", "CARRIERDELAY", "LATEAIRCRAFTDELAY"
]

# Numeric-only columns
numeric_cols = [
    "DEPDELAY", "ARRDELAY", "WEATHERDELAY", "NASDELAY", "CARRIERDELAY", "LATEAIRCRAFTDELAY"
]

all_data = []

for file in csv_files:
    print(f"Reading {file}")
    df = pd.read_csv(file, low_memory=False)

    # Standardize column names
    df.columns = df.columns.str.strip().str.upper()

    # Make everything match the uppercase version
    columns = [col.upper() for col in columns_to_keep]
    numeric = [col.upper() for col in numeric_cols]

    # Keep available columns
    available_cols = [col for col in columns if col in df.columns]
    df = df[available_cols]

    # Convert numeric columns
    for col in numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    all_data.append(df)

# Combine and save
combined = pd.concat(all_data, ignore_index=True)
output_path = os.path.join(output_dir, "on_time_cleaned_2023_Jul_Dec.csv")
combined.to_csv(output_path, index=False)
print(f"\n✅ Saved cleaned data to: {output_path}")
