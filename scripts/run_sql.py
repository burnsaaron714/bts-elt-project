import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data/processed/flights.db")

# SQL query (copy-paste from before)
query = """
SELECT
    REPORTING_AIRLINE AS carrier,
    strftime('%Y-%m', FLIGHTDATE) AS flight_month,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN DEPDELAY > 15 THEN 1 ELSE 0 END) AS delayed_flights,
    ROUND(AVG(DEPDELAY), 2) AS avg_dep_delay,
    ROUND(AVG(ARRDELAY), 2) AS avg_arr_delay
FROM on_time_flights
WHERE CANCELLED = 0
GROUP BY carrier, flight_month
ORDER BY flight_month, carrier;
"""

# Run the query and show results
df = pd.read_sql_query(query, conn)
print(df.head())

# Close connection
conn.close()
