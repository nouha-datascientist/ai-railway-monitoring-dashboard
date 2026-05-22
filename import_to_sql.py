import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("railway_data.csv")

# Connect to database
conn = sqlite3.connect("railway.db")

# Export dataframe into SQL table
df.to_sql(
    "railway_telemetry",
    conn,
    if_exists="replace",
    index=False
)

print("Telemetry data imported successfully.")

conn.close()