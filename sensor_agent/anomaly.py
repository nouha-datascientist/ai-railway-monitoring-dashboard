# =========================================
# SENSOR AGENT
# =========================================

print("=== SENSOR AGENT ===")

# Simulated vibration sensor readings
vibration = [0.20, 0.21, 0.22, 0.23, 0.24, 0.90]

# Historical readings (excluding latest)
historical = vibration[:-1]

# Latest sensor value
latest_value = vibration[-1]

# Compute statistics
mean = np.mean(historical)
std = np.std(historical)

# Compute Z-score
z_score = (latest_value - mean) / std

print(f"Mean vibration: {mean:.2f}")
print(f"Standard deviation: {std:.4f}")
print(f"Latest value: {latest_value:.2f}")
print(f"Z-score: {z_score:.2f}")

# Threshold for anomaly
threshold = 3

if abs(z_score) > threshold:
    anomaly_detected = True
    anomaly_text = "Critical turbine vibration anomaly detected."
    print("ALERT:", anomaly_text)
else:
    anomaly_detected = False
    print("System operating normally.")