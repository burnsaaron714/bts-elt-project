#!/usr/bin/env python3

import subprocess

print("🚀 Starting extraction...", flush=True)
subprocess.run(["python3", "-u", "scripts/extract.py"], check=True)

print("\n🧹 Cleaning and transforming data...", flush=True)
subprocess.run(["python3", "-u", "scripts/transform.py"], check=True)

print("\n💾 Loading cleaned data into SQLite...", flush=True)
subprocess.run(["python3", "-u", "scripts/load.py"], check=True)

print("\n📊 Running SQL summary query...", flush=True)
subprocess.run(["python3", "-u", "scripts/run_sql.py"], check=True)

print("\n✅ Pipeline complete.", flush=True)