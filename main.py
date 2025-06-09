#!/usr/bin/env python3

import subprocess

def main():
    # Step 1: Extract raw data
    print("Starting extraction...", flush=True)
    subprocess.run(["python3", "-u", "scripts/extract.py"], check=True)

    # Step 2: Clean and transform data
    print("\nCleaning and transforming data...", flush=True)
    subprocess.run(["python3", "-u", "scripts/transform.py"], check=True)

    # Step 3: Load cleaned data into SQLite
    print("\nLoading cleaned data into SQLite...", flush=True)
    subprocess.run(["python3", "-u", "scripts/load.py"], check=True)

    # Step 4: Run SQL summary queries
    print("\nRunning SQL summary query...", flush=True)
    subprocess.run(["python3", "-u", "scripts/run_sql.py"], check=True)

    print("\nPipeline complete.", flush=True)

if __name__ == "__main__":
    main()