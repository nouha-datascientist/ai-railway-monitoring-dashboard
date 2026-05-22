import sqlite3
import pandas as pd
import random
import time
from datetime import datetime

# Connect to SQLite
conn = sqlite3.connect("railway.db")

cursor = conn.cursor()

train_ids = ["TR001", "TR002", "TR003"]

while True:

    train_id = random.choice(train_ids)

    vibration = round(random.uniform(0.2, 0.9), 2)

    temperature = round(random.uniform(25, 75), 2)

    if vibration > 0.7:
        anomaly = "Critical"
        maintenance = "Inspection Required"
    else:
        anomaly = "Normal"
        maintenance = "Normal"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO railway_telemetry (
            Train_ID,
            Timestamp,
            Vibration,
            Temperature,
            Anomaly_Status,
            Maintenance_Status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        train_id,
        timestamp,
        vibration,
        temperature,
        anomaly,
        maintenance
    ))

    conn.commit()

    print(
        f"Inserted: {train_id} | "
        f"Vibration={vibration} | "
        f"Temp={temperature}"
    )

    time.sleep(5)