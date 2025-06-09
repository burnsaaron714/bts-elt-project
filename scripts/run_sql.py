import sqlite3
import pandas as pd
from blob_utils import upload_file_to_blob  # Import Azure upload utility

def main():
    # Connect to the SQLite database
    db_path = "data/processed/flights.db"
    conn = sqlite3.connect(db_path)

    # 1. Total Flights and Delayed Flights by Airline
    query1 = """
    SELECT
        REPORTING_AIRLINE AS carrier,
        COUNT(*) AS total_flights,
        SUM(CASE WHEN DEPDELAY > 15 THEN 1 ELSE 0 END) AS delayed_flights
    FROM flights
    WHERE CANCELLED = 0
    GROUP BY carrier
    ORDER BY delayed_flights DESC;
    """
    df1 = pd.read_sql_query(query1, conn)
    print("Total Flights and Delayed Flights by Airline:")
    print(df1, end="\n\n")
    out1 = "data/processed/total_flights_and_delayed_by_airline.csv"
    df1.to_csv(out1, index=False)
    upload_file_to_blob(out1, "total_flights_and_delayed_by_airline.csv")

    # 2. NAS Delay Summary by Airport
    # Shows airports with the most NAS delay minutes, only for airports with >10,000 flights
    query2 = """
    SELECT
        ORIGIN AS airport,
        COUNT(*) AS total_flights,
        SUM(CASE WHEN NASDELAY > 0 THEN 1 ELSE 0 END) AS flights_with_nas_delay,
        SUM(NASDELAY) AS total_nas_delay_minutes,
        ROUND(AVG(CASE WHEN NASDELAY > 0 THEN NASDELAY END), 2) AS avg_nas_delay_per_delayed_flight
    FROM flights
    WHERE CANCELLED = 0
    GROUP BY airport
    HAVING COUNT(*) > 10000  -- Only show airports with more than 10,000 flights for meaningful averages
    ORDER BY total_nas_delay_minutes DESC;
    """
    df2 = pd.read_sql_query(query2, conn)
    print("NAS Delay Summary by Airport (min 10,000 flights):")
    print(df2, end="\n\n")
    out2 = "data/processed/nas_delay_summary_by_airport.csv"
    df2.to_csv(out2, index=False)
    upload_file_to_blob(out2, "nas_delay_summary_by_airport.csv")

    # 3. Airports with the Longest Average Departure Delays
    # Lists top 5 airports with the highest average departure delay, only if they have >10,000 flights
    query3 = """
    SELECT
        ORIGIN AS airport,
        ROUND(AVG(DEPDELAY), 2) AS avg_dep_delay,
        COUNT(*) AS total_flights
    FROM flights
    WHERE CANCELLED = 0
    GROUP BY airport
    HAVING COUNT(*) > 10000
    ORDER BY avg_dep_delay DESC
    LIMIT 5;
    """
    df3 = pd.read_sql_query(query3, conn)
    print("Top 5 Airports with the Longest Average Departure Delays (min 10,000 flights):")
    print(df3, end="\n\n")
    out3 = "data/processed/top5_airports_longest_avg_dep_delay.csv"
    df3.to_csv(out3, index=False)
    upload_file_to_blob(out3, "top5_airports_longest_avg_dep_delay.csv")

    # 4. Average Delay by Airline
    # Shows average departure and arrival delay for each airline
    query4 = """
    SELECT
        REPORTING_AIRLINE AS carrier,
        ROUND(AVG(DEPDELAY), 2) AS avg_dep_delay,
        ROUND(AVG(ARRDELAY), 2) AS avg_arr_delay
    FROM flights
    WHERE CANCELLED = 0
    GROUP BY carrier
    ORDER BY avg_arr_delay DESC;
    """
    df4 = pd.read_sql_query(query4, conn)
    print("Average Delay by Airline:")
    print(df4, end="\n\n")
    out4 = "data/processed/average_delay_by_airline.csv"
    df4.to_csv(out4, index=False)
    upload_file_to_blob(out4, "average_delay_by_airline.csv")

    # 5. Routes with the Longest Average Arrival Delays
    # Shows top 10 routes (origin -> destination) with the highest average arrival delay, only if >1,000 flights
    query5 = """
    SELECT
        ORIGIN || ' -> ' || DEST AS route,
        COUNT(*) AS total_flights,
        ROUND(AVG(ARRDELAY), 2) AS avg_arr_delay
    FROM flights
    WHERE CANCELLED = 0
    GROUP BY route
    HAVING COUNT(*) > 1000  -- Only show routes with more than 1,000 flights for meaningful averages
    ORDER BY avg_arr_delay DESC
    LIMIT 10;
    """
    df5 = pd.read_sql_query(query5, conn)
    print("Routes with the Longest Average Arrival Delays (min 1,000 flights):")
    print(df5, end="\n\n")
    out5 = "data/processed/routes_longest_avg_arr_delay.csv"
    df5.to_csv(out5, index=False)
    upload_file_to_blob(out5, "routes_longest_avg_arr_delay.csv")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
