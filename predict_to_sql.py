import pandas as pd
import sqlite3

# Load telemetry data
df = pd.read_csv("railway_data.csv")

# Simple AI prediction logic
def predict_risk(vibration):
    if vibration > 0.7:
        return "High Risk", 0.9
    elif vibration > 0.4:
        return "Medium Risk", 0.6
    else:
        return "Low Risk", 0.2

# Generate predictions
predictions = []

for _, row in df.iterrows():
    prediction, score = predict_risk(row["Vibration"])

    predictions.append({
        "Train_ID": row["Train_ID"],
        "Timestamp": row["Timestamp"],
        "AI_Prediction": prediction,
        "Risk_Score": score
    })

pred_df = pd.DataFrame(predictions)

# Connect to SQLite
conn = sqlite3.connect("railway.db")

# Export predictions to SQL
pred_df.to_sql(
    "railway_predictions",
    conn,
    if_exists="replace",
    index=False
)

print("AI predictions exported to SQL successfully.")

conn.close()