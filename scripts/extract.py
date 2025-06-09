#!/usr/bin/env python3

import os
import requests
import zipfile
from io import BytesIO

def main():
    # Configuration
    year = 2023
    months = range(7, 13)  # July (7) to December (12)
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each month and download the corresponding ZIP file
    for month in months:
        # {month:02d} formats the month as two digits (07,08,09)
        url = (
            f"https://transtats.bts.gov/PREZIP/"
            f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
        )
        print(f"\nDownloading: {url}")

        try:
            response = requests.get(url)
            if response.status_code == 404:
                print(f"404 Not found: {url}")
                continue

            response.raise_for_status()  # Raises an error for bad responses

            # Extract ZIP contents in memory using BytesIO
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                for file_name in z.namelist():
                    if file_name.endswith(".csv"):
                        # Save as on_time_performance_2023_07.csv, etc.
                        out_path = os.path.join(
                            output_dir, f"on_time_performance_{year}_{month:02d}.csv"
                        )
                        if not os.path.exists(out_path):
                            with open(out_path, "wb") as f_out:
                                f_out.write(z.read(file_name))
                            print(f"Extracted to: {out_path}")
                        else:
                            print(f"Already exists: {out_path}")

        except requests.RequestException as e:
            print(f"Network error processing {year}-{month:02d}: {e}")
        except zipfile.BadZipFile:
            print(f"Bad ZIP file for {year}-{month:02d}")
        except Exception as e:
            print(f"Error processing {year}-{month:02d}: {e}")

if __name__ == "__main__":
    main()
