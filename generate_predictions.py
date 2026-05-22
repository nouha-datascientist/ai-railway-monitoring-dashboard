import pandas as pd

# Load telemetry data
df = pd.read_csv("railway_data.csv")

# Simple AI-inspired prediction logic
def predict_failure(vibration, temperature):
    score = (vibration * 100) + (temperature * 0.5)

    if score >= 100:
        return "High Risk"
    elif score >= 50:
        return "Medium Risk"
    else:
        return "Low Risk"

# Generate predictions
df["AI_Prediction"] = df.apply(
    lambda row: predict_failure(row["Vibration"], row["Temperature"]),
    axis=1
)

# Save updated dataset
df.to_csv("railway_predictions.csv", index=False)

print("Predictions generated successfully.")