import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest

# Load telemetry data
df = pd.read_csv("railway_data.csv")

# Features for anomaly detection
features = df[["Vibration", "Temperature"]]

# Train Isolation Forest
model = IsolationForest(
    contamination=0.2,
    random_state=42
)

model.fit(features)

# Predict anomalies
predictions = model.predict(features)

# Convert predictions
df["ML_Anomaly"] = predictions

# Replace:
# -1 → Critical
#  1 → Normal

df["ML_Anomaly"] = df["ML_Anomaly"].replace({
    -1: "Critical",
     1: "Normal"
})

# Business safety override
df.loc[df["Vibration"] > 0.7, "ML_Anomaly"] = "Critical"

# Connect to SQLite
conn = sqlite3.connect("railway.db")

# Export ML results
df.to_sql(
    "ml_telemetry_analysis",
    conn,
    if_exists="replace",
    index=False
)

print("ML anomaly analysis exported successfully.")

conn.close()