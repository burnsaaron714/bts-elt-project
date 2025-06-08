#!/usr/bin/env python3

import os

# Step 1: Extract data
print("🚀 Starting extraction...")
os.system("python3 scripts/extract.py")

# Step 2: Transform data
print("\n🧹 Cleaning and transforming data...")
os.system("python3 scripts/transform.py")

# Step 3: Load into SQLite
print("\n💾 Loading cleaned data into SQLite...")
os.system("python3 scripts/load.py")

# Step 4: Run SQL query and print summary
print("\n📊 Running SQL summary query...")
os.system("python3 scripts/run_sql.py")

print("\n✅ Pipeline complete.")
# This script orchestrates the entire ETL pipeline: