# BTS Flight Delay ETL Project

This is a simple ETL/ELT pipeline built with Python that processes U.S. Department of Transportation (BTS) On-Time Performance data from July–December 2023. The goal is to extract flight delay data, clean it, load it into a SQLite database, and generate a monthly delay summary by airline using SQL.

## 📌 What the Project Does

- **Extract** raw CSVs from BTS.gov ZIP archives
- **Transform** and filter the data to keep relevant columns
- **Load** the cleaned data into a SQLite database
- **Query** using SQL to summarize delays by month and airline

## 🧰 Tech Stack

- Python (pandas, sqlite3)
- SQLite (local file-based DB)
- Shell/CLI for orchestration
- GitHub for version control

## 📁 Folder Structure

```
de_project/
├── data/
│   ├── raw/                # Original CSVs from BTS
│   └── processed/          # Cleaned CSV + SQLite DB
├── scripts/
│   ├── extract.py          # Downloads and unzips BTS data
│   ├── transform.py        # Filters and cleans columns
│   ├── load.py             # Writes to SQLite database
│   └── run_sql.py          # SQL summary: flights, delays, averages
├── main.py                 # Orchestrates full pipeline
├── .gitignore
└── README.md
```

## 🚀 How to Run the Project

1. Clone the repo:
   ```bash
   git clone https://github.com/burnsaaron714/bts-elt-project.git
   cd bts-elt-project
   ```

2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pandas
   ```

3. Run the full pipeline:
   ```bash
   python3 main.py
   ```

4. Results will be printed to terminal and saved in:
   - `data/processed/on_time_cleaned_2023_Jul_Dec.csv`
   - `data/processed/flights.db`

## 📊 Output Sample (SQL Summary)

| Airline | Month     | Flights | Delayed | Avg Dep Delay | Avg Arr Delay |
|---------|-----------|---------|---------|----------------|----------------|
| AA      | 2023-07   | 15000   | 3500    | 12.7           | 10.3           |

> Only non-cancelled flights are included. A flight is considered delayed if departure delay > 15 minutes.

## ✅ Purpose

This project is designed to demonstrate:
- Clean ETL structure across scripts
- Use of SQL for analytics
- Good folder hygiene and Git workflow
- Beginner-friendly pipeline you can run end-to-end

## 🙋‍♂️ Author

Aaron Burns  
[GitHub Profile](https://github.com/burnsaaron714)
