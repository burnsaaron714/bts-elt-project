#!/usr/bin/env python3

import os
import pandas as pd
import sqlite3

# Input cleaned CSV
input_path = os.path.join("data", "processed", "on_time_cleaned_2023_Jul_Dec.csv")

# Output DB file
db_path = os.path.join("data", "processed", "flights.db")
table_name = "on_time_flights"

# Read the cleaned CSV
print(f"📄 Loading CSV: {input_path}")
df = pd.read_csv(input_path)

# Open SQLite connection
print(f"🗃️ Saving to SQLite: {db_path}")
conn = sqlite3.connect(db_path)

# Save to table (overwrite if it exists)
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Done
conn.close()
print(f"✅ Data saved to table '{table_name}' in {db_path}")
