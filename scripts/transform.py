#!/usr/bin/env python3

import os
import glob
import pandas as pd
from blob_utils import upload_file_to_blob  # Import Azure upload utility

def main():
    """
    Reads raw CSV files of flight data, selects relevant columns, 
    converts certain columns to numeric, and saves a cleaned combined CSV.
    """
    # Set input and output directories
    raw_dir = "data/raw"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    # Find all relevant CSV files in the raw data directory
    csv_pattern = os.path.join(raw_dir, "on_time_performance_2023_*.csv")
    csv_files = sorted(glob.glob(csv_pattern))
    print(f"\nFound {len(csv_files)} CSV files.")

    if not csv_files:
        print("No CSV files found. Exiting.")
        return

    # List of columns to keep
    columns_to_keep = [
        # Flight info
        "FLIGHTDATE", "REPORTING_AIRLINE", "TAIL_NUMBER", "ORIGIN", "DEST",
        # Delay and cancellation info
        "DEPDELAY", "ARRDELAY", "CANCELLED", "CANCELLATIONCODE",
        "WEATHERDELAY", "NASDELAY", "CARRIERDELAY", "LATEAIRCRAFTDELAY"
    ]

    # Columns that should be numeric
    numeric_cols = [
        "DEPDELAY", "ARRDELAY", "WEATHERDELAY", "NASDELAY", "CARRIERDELAY", "LATEAIRCRAFTDELAY"
    ]

    all_data = []

    # Process each CSV file
    for file_path in csv_files:
        print(f"\nReading {file_path}")
        df = pd.read_csv(file_path, low_memory=False)

        # Standardize column names: remove spaces and make uppercase for consistency
        df.columns = df.columns.str.strip().str.upper()

        # Keep only the columns we care about (if they exist in this file)
        available_cols = [col for col in columns_to_keep if col in df.columns]
        df = df[available_cols]

        # Convert delay columns to numeric, coercing errors to NaN (e.g., if data is missing or invalid)
        for col in numeric_cols:
            if col in df.columns:
                df.loc[:, col] = pd.to_numeric(df[col], errors="coerce")

        all_data.append(df)

    # Combine all DataFrames into one
    combined = pd.concat(all_data, ignore_index=True)

    # Save the cleaned, combined data to a new CSV file
    output_path = os.path.join(output_dir, "on_time_cleaned_2023_Jul_Dec.csv")
    combined.to_csv(output_path, index=False)
    print(f"\nSaved cleaned data to: {output_path}")

    # Upload the cleaned CSV to Azure Blob Storage
    upload_file_to_blob(
        output_path,
        os.path.basename(output_path)  # Use the filename as the blob name
    )

# This ensures main() only runs if this script is executed directly
if __name__ == "__main__":
    main()
