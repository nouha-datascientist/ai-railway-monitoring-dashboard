import subprocess
import time

while True:

    print("\n🔄 Running ML anomaly analysis...")

    subprocess.run(
        ["venv\\Scripts\\python.exe", "ml_anomaly_detection.py"]
    )

    print("\n📈 Running forecasting engine...")

    subprocess.run(
        ["venv\\Scripts\\python.exe", "forecast_vibration.py"]
    )

    print("\n✅ AI pipelines refreshed.")

    time.sleep(60)