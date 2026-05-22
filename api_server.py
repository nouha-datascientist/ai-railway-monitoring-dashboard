from fastapi import FastAPI
import sqlite3
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Railway AI Monitoring API Running"}

@app.get(
    "/telemetry",
    summary="Retrieve railway telemetry data",
    description="Returns telemetry records from the railway monitoring system."
)
def get_telemetry(
    train_id: str = None,
    anomaly: str = None,
    limit: int = 10
):

    conn = sqlite3.connect("railway.db")

    query = "SELECT * FROM railway_telemetry WHERE 1=1"

    if train_id:
        query += f" AND Train_ID = '{train_id}'"

    if anomaly:
        query += f" AND Anomaly_Status = '{anomaly}'"

    query += f" LIMIT {limit}"

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df.to_dict(orient="records")
@app.get(
    "/ml-anomalies",
    summary="Retrieve critical ML anomalies",
    description="Returns machine learning detected critical anomalies."
)
def get_ml_anomalies():

    conn = sqlite3.connect("railway.db")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM ml_telemetry_analysis
        WHERE ML_Anomaly = 'Critical'
        """,
        conn
    )

    conn.close()

    return df.to_dict(orient="records")

@app.get(
    "/analytics/summary",
    summary="Operational analytics summary",
    description="Returns aggregated telemetry KPIs."
)
def analytics_summary():

    conn = sqlite3.connect("railway.db")

    total_records = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM railway_telemetry",
        conn
    )["total"][0]

    critical_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS critical_count
        FROM railway_telemetry
        WHERE Anomaly_Status = 'Critical'
        """,
        conn
    )["critical_count"][0]

    avg_vibration = pd.read_sql_query(
        """
        SELECT AVG(Vibration) AS avg_vibration
        FROM railway_telemetry
        """,
        conn
    )["avg_vibration"][0]

    avg_temperature = pd.read_sql_query(
        """
        SELECT AVG(Temperature) AS avg_temperature
        FROM railway_telemetry
        """,
        conn
    )["avg_temperature"][0]

    conn.close()

    return {
    "total_records": int(total_records),
    "critical_anomalies": int(critical_count),
    "average_vibration": float(round(avg_vibration, 2)),
    "average_temperature": float(round(avg_temperature, 2))
}