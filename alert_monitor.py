import sqlite3
import pandas as pd
import time

seen_ids = set()

while True:

    conn = sqlite3.connect("railway.db")

    df = pd.read_sql_query(
        """
        SELECT rowid, *
        FROM railway_telemetry
        WHERE Anomaly_Status = 'Critical'
        """,
        conn
    )

    conn.close()

    for _, row in df.iterrows():

        if row["rowid"] not in seen_ids:

            print("\n🚨 ALERT 🚨")
            print(f"Train: {row['Train_ID']}")
            print(f"Vibration: {row['Vibration']}")
            print(f"Temperature: {row['Temperature']}")
            print(f"Timestamp: {row['Timestamp']}")

            seen_ids.add(row["rowid"])

    time.sleep(5)