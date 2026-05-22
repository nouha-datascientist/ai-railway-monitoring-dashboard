import subprocess

processes = []

scripts = [
    ["python", "live_telemetry_stream.py"],
    ["python", "alert_monitor.py"],
    ["uvicorn", "api_server:app", "--reload"]
]

for script in scripts:

    process = subprocess.Popen(script)

    processes.append(process)

print("🚀 Railway AI Monitoring System Running")

for process in processes:
    process.wait()