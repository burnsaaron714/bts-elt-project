# BTS Flight Delay ETL Pipeline

This is an ETL pipeline built with Python that processes U.S. Department of Transportation - Bureau of Transportation Statistics (BTS) on time flight performance data from July–December 2023. The goal is to extract flight delay data, clean it, load it into a SQLite database, and generate a monthly delay summary by airline using SQL.

## Project Purpose

I built this project to sharpen my data engineering skills for interview prep. I wanted to simulate an ETL pipeline using real-world aviation data from the Department of Transportation (BTS).

## Method 

- Extract raw CSVs from BTS.gov ZIP archives
- Transform and filter the data to keep relevant columns
- Load the cleaned data into a SQLite database
- Query using SQL to summarize delays by month and airline

## Tech Stack

- Python (pandas, sqlite3)
- SQLite (local file-based DB)
- Azure Blob Storage (cloud file storage)
- CLI for orchestration
- GitHub for version control

## Folder Structure

```
de_project/
├── data/
│   ├── raw/                # Original CSVs from BTS (also uploaded to Azure Blob Storage)
│   └── processed/          # Cleaned CSV + SQLite DB (also uploaded to Azure Blob Storage)
├── scripts/
│   ├── extract.py          # Downloads and unzips BTS data, uploads to Azure
│   ├── transform.py        # Filters and cleans columns, uploads to Azure
│   ├── load.py             # Downloads cleaned CSV from Azure if not present
│   ├── run_sql.py          # SQL summary: flights, delays, averages (uploads results to Azure)
│   └── blob_utils.py       # Azure Blob Storage utility functions
├── main.py                 # Orchestrates full pipeline
├── .env                    # Azure credentials (not tracked in git)
├── .gitignore
└── README.md
```

## How to Run the Project

1. Clone the repo:
   ```bash
   git clone https://github.com/burnsaaron714/bts-elt-project.git
   cd bts-elt-project
   ```

2. **Create a `.env` file in the project root with your Azure credentials:**
   ```
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
   AZURE_CONTAINER_NAME=your_container_name_here
   ```

3. **Install dependencies:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run the full pipeline:
   ```bash
   python3 main.py
   ```

4. Results will be printed to terminal and saved in:
   - `data/processed/on_time_cleaned_2023_Jul_Dec.csv`
   - `data/processed/flights.db`
   - SQL summary CSVs in `data/processed/` (also uploaded to Azure Blob Storage)

## Azure Blob Storage

**What is Azure Blob Storage used for in this project?**

Azure Blob Storage is a cloud-based storage solution that allows this pipeline to:
- **Upload** raw and processed data files for backup, sharing, and reproducibility.
- **Download** required files if they are not present locally, enabling the pipeline to run from any environment.
- **Upload SQL summary results** for remote access or further analysis.

This makes the pipeline cloud-friendly, portable, and suitable for collaboration or deployment in production environments.

**Azure Blob Storage setup**

1. **Create a `.env` file in the project root with:**
   ```
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
   AZURE_CONTAINER_NAME=your_container_name_here
   ```

2. **Install dependencies:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the pipeline with Azure support:**
   ```bash
   python3 main.py --azure
   ```

## Output Sample (SQL Summary)

### Total Flights and Delayed Flights by Airline

| Airline | Total Flights | Delayed Flights |
|---------|--------------|----------------|
| AA      | 15000        | 3500           |

### NAS Delay Summary by Airport

| Airport | Total Flights | Flights with NAS Delay | Total NAS Delay Minutes | Avg NAS Delay (Delayed Flights) |
|---------|--------------|-----------------------|------------------------|-------------------------------|
| ATL     | 12000        | 800                   | 5400                   | 6.75                          |

### Top 5 Airports with Longest Avg Departure Delays

| Airport | Avg Dep Delay | Total Flights |
|---------|---------------|--------------|
| JFK     | 14.2          | 12000        |

### Average Delay by Airline

| Airline | Avg Dep Delay | Avg Arr Delay |
|---------|---------------|---------------|
| AA      | 12.7          | 10.3          |

### Routes with Longest Avg Arrival Delays

| Route         | Total Flights | Avg Arr Delay |
|---------------|--------------|---------------|
| JFK -> LAX    | 2000         | 18.5          |

> Only non-cancelled flights are included. A flight is considered delayed if departure delay > 15 minutes.

## Author

Aaron Burns  
[GitHub Profile](https://github.com/burnsaaron714)
