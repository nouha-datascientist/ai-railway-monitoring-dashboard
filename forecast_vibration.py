import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load telemetry data
df = pd.read_csv("railway_data.csv")

# Create numerical timeline
df["Time_Index"] = np.arange(len(df))

# Features and target
X = df[["Time_Index"]]
y = df["Vibration"]

# Train forecasting model
model = LinearRegression()
model.fit(X, y)

# Predict future points
future_index = np.arange(len(df), len(df) + 5).reshape(-1, 1)

future_predictions = model.predict(future_index)

# Create forecast dataframe
forecast_df = pd.DataFrame({
    "Future_Time_Index": future_index.flatten(),
    "Predicted_Vibration": future_predictions
})

# Save to SQLite
conn = sqlite3.connect("railway.db")

forecast_df.to_sql(
    "vibration_forecast",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

# Plot forecast
plt.plot(df["Time_Index"], y, label="Historical Vibration")
plt.plot(
    future_index,
    future_predictions,
    label="Forecasted Vibration"
)

plt.xlabel("Time Index")
plt.ylabel("Vibration")
plt.title("Vibration Forecast")
plt.legend()

plt.show()

print("Forecast exported successfully.")