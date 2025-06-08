#!/usr/bin/env python3

import os
import requests
import zipfile
from io import BytesIO

# Config
year = 2023
months = range(7, 13)  # July to December
output_dir = os.path.join("data", "raw")
os.makedirs(output_dir, exist_ok=True)

# Loop through each month
for month in months:
    # Use correct BTS URL format
    url = f"https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"

    print(f"\n📡 Downloading: {url}")

    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"❌ Not found: {url}")
            continue

        response.raise_for_status()

        # Extract ZIP contents
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            for file_name in z.namelist():
                if file_name.endswith(".csv"):
                    out_path = os.path.join(output_dir, f"on_time_performance_{year}_{month:02d}.csv")
                    if not os.path.exists(out_path):
                        with open(out_path, "wb") as f_out:
                            f_out.write(z.read(file_name))
                        print(f"✅ Extracted to: {out_path}")
                    else:
                        print(f"⚠️ Already exists: {out_path}")

    except Exception as e:
        print(f"❗ Error processing {year}-{month:02d}: {e}")
