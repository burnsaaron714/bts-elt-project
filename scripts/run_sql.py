import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data/processed/flights.db")

# 1. Total Flights and Delayed Flights by Airline
query1 = """
SELECT
    REPORTING_AIRLINE AS carrier,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN DEPDELAY > 15 THEN 1 ELSE 0 END) AS delayed_flights
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY carrier
ORDER BY delayed_flights DESC;
"""
df1 = pd.read_sql_query(query1, conn)
print("Total Flights and Delayed Flights by Airline:")
print(df1, end="\n\n")

# 2. NAS Delay Summary by Airport (average only for delayed flights)
query2 = """
SELECT
    ORIGIN AS airport,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN NASDELAY > 0 THEN 1 ELSE 0 END) AS flights_with_nas_delay,
    SUM(NASDELAY) AS total_nas_delay_minutes,
    ROUND(AVG(CASE WHEN NASDELAY > 0 THEN NASDELAY END), 2) AS avg_nas_delay_per_delayed_flight
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY airport
HAVING COUNT(*) > 10000  -- Only show airports with more than 10000 flights for meaningful averages
ORDER BY total_nas_delay_minutes DESC;
"""
df2 = pd.read_sql_query(query2, conn)
print("NAS Delay Summary by Airport (min 10000 flights):")
print(df2, end="\n\n")

# 3. Airports with the Longest Average Departure Delays
query3 = """
SELECT
    ORIGIN AS airport,
    ROUND(AVG(DEPDELAY), 2) AS avg_dep_delay,
    COUNT(*) AS total_flights
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY airport
HAVING COUNT(*) > 10000  -- Only show airports with more than 10000 flights for meaningful averages
ORDER BY avg_dep_delay DESC
LIMIT 5;
"""
df3 = pd.read_sql_query(query3, conn)
print("Top 5 Airports with the Longest Average Departure Delays (min 10000 flights):")
print(df3, end="\n\n")

# 4. Average Delay by Airline
query4 = """
SELECT
    REPORTING_AIRLINE AS carrier,
    ROUND(AVG(DEPDELAY), 2) AS avg_dep_delay,
    ROUND(AVG(ARRDELAY), 2) AS avg_arr_delay
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY carrier
ORDER BY avg_arr_delay DESC;
"""
df4 = pd.read_sql_query(query4, conn)
print("Average Delay by Airline:")
print(df4, end="\n\n")

# 5. Routes with the Longest Average Arrival Delays (includes route: ORIGIN -> DEST)
query5 = """
SELECT
    ORIGIN || ' -> ' || DEST AS route,
    COUNT(*) AS total_flights,
    ROUND(AVG(ARRDELAY), 2) AS avg_arr_delay
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY route
HAVING COUNT(*) > 1000  -- Only show routes with more than 1000 flights for meaningful averages
ORDER BY avg_arr_delay DESC
LIMIT 10;
"""
df5 = pd.read_sql_query(query5, conn)
print("Routes with the Longest Average Arrival Delays (min 1000 flights):")
print(df5, end="\n\n")

# Close connection
conn.close()
