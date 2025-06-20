#!/usr/bin/env python3

import os
import pandas as pd
import sqlite3
from blob_utils import download_blob_to_file  # Import Azure download utility

def main():
    """
    Loads the cleaned flight data CSV into a SQLite database table.
    """
    # Path to the cleaned CSV file
    input_path = os.path.join("data", "processed", "on_time_cleaned_2023_Jul_Dec.csv")
    blob_name = "on_time_cleaned_2023_Jul_Dec.csv"

    # Download the cleaned CSV from Azure Blob Storage if not present locally
    if not os.path.exists(input_path):
        print(f"Downloading {blob_name} from Azure Blob Storage...")
        download_blob_to_file(blob_name, input_path)

    # Path to the SQLite database file
    db_path = os.path.join("data", "processed", "flights.db")
    table_name = "flights"

    # Read the cleaned CSV into a DataFrame
    print(f"\nLoading CSV: {input_path}")
    df = pd.read_csv(input_path)

    # Connect to SQLite database 
    print(f"Saving to SQLite: {db_path}")
    conn = sqlite3.connect(db_path)

    # Save DataFrame to a SQL table. Overwrite if the table already exists
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Close the connection
    conn.close()
    print(f"Data saved to table '{table_name}' in {db_path}")

if __name__ == "__main__":
    main()
