import matplotlib.pyplot as plt
import gradio as gr
import numpy as np
import random
import time
import pandas as pd
from datetime import datetime
import os
def sensor_agent():

    # Initial readings
    vibration_history = [0.20, 0.21, 0.22, 0.23, 0.24]

    # Generate new reading
    new_value = random.uniform(0.20, 0.25)

    # Inject anomaly occasionally
    if random.random() < 0.2:
        new_value = 0.90

    vibration_history.append(new_value)

    return vibration_history, new_value
def analysis_agent(vibration_history, new_value):

    rolling_window = vibration_history[-5:]

    mean = np.mean(rolling_window)
    std = np.std(rolling_window)

    if std == 0:
        std = 0.0001

    z_score = (new_value - mean) / std

    previous_value = vibration_history[-2]
    rate_of_change = new_value - previous_value

    x = np.arange(len(rolling_window))
    slope, intercept = np.polyfit(x, rolling_window, 1)

    future_step = len(rolling_window) + 3
    predicted_vibration = slope * future_step + intercept

    anomaly_score = 0

    if abs(z_score) > 3:
        anomaly_score += 1

    if abs(rate_of_change) > 0.30:
        anomaly_score += 1

    if slope > 0.02:
        anomaly_score += 1

    if predicted_vibration > 0.50:
        anomaly_score += 1

    return {
        "mean": mean,
        "std": std,
        "z_score": z_score,
        "rate_of_change": rate_of_change,
        "slope": slope,
        "predicted_vibration": predicted_vibration,
        "anomaly_score": anomaly_score
    }  
def logging_agent(
    vibration,
    z_score,
    predicted_vibration,
    anomaly_score,
    status
):

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vibration": vibration,
        "z_score": z_score,
        "predicted_vibration": predicted_vibration,
        "anomaly_score": anomaly_score,
        "status": status
    }

    df = pd.DataFrame([log_entry])

    log_file = "system_logs.csv"

    # Create file if it doesn't exist
    if not os.path.exists(log_file):
        df.to_csv(log_file, index=False)

    else:
        df.to_csv(
            log_file,
            mode='a',
            header=False,
            index=False
        )
def supervisor_agent():

    print("\n=== SUPERVISOR AGENT ===")
    print("Coordinating operational AI agents...")

    # Sensor Agent
    vibration_history, new_value = sensor_agent()

    print("Sensor Agent completed.")

    # Analysis Agent
    analysis = analysis_agent(
        vibration_history,
        new_value
    )

    print("Analysis Agent completed.")

    return vibration_history, new_value, analysis
def monitor_system():
    # Supervisor Agent
    vibration_history, new_value, analysis = supervisor_agent()

    # Use the analysis results directly from the supervisor workflow
    anomaly_score = analysis["anomaly_score"]

    if anomaly_score >= 2:
        status = "🚨 CRITICAL ANOMALY DETECTED"
        retrieved_doc = """
        High vibration levels may indicate bearing degradation.
        Inspect turbine bearings immediately.
        """
        recommendation = """
        Recommend immediate turbine shutdown and bearing inspection.
        """
    else:
        status = "✅ System Operating Normally"
        retrieved_doc = "No maintenance action required."
        recommendation = "Continue normal operations."

    # Logging Agent
    logging_agent(
        new_value,
        analysis["z_score"],
        analysis["predicted_vibration"],
        analysis["anomaly_score"],
        status
    )

    # Create chart
    fig, ax = plt.subplots()
    ax.plot(vibration_history, marker='o')
    ax.set_title("Live Turbine Vibration Monitoring")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Vibration")

    if anomaly_score >= 2:
        ax.scatter(
            len(vibration_history) - 1,
            new_value,
            s=100
        )

    plt.close(fig)

    agent_status = """
    ✅ Supervisor Agent Active
    ✅ Sensor Agent Active
    ✅ Analysis Agent Active
    ✅ Logging Agent Active
    ✅ Recommendation Agent Active
    """

    return (
        fig,
        f"{new_value:.2f}",
        f"{analysis['mean']:.2f}",
        f"{analysis['std']:.4f}",
        f"{analysis['z_score']:.2f}",
        f"{analysis['rate_of_change']:.2f}",
        f"{analysis['slope']:.4f}",
        f"{analysis['predicted_vibration']:.2f}",
        f"{analysis['anomaly_score']}",
        agent_status,
        status,
        retrieved_doc,
        recommendation
    )

# Build UI
with gr.Blocks(
    title="Sovereign AI Infrastructure Monitoring"
) as dashboard:

    gr.Markdown(
        """
        # 🧠 Sovereign Multi-Agent AI System
        ### Predictive Infrastructure Operations Platform
        """
    )

    with gr.Row():

        vibration_box = gr.Textbox(
            label="Current Vibration"
        )

        prediction_box = gr.Textbox(
            label="Predicted Vibration"
        )

        anomaly_box = gr.Textbox(
            label="Anomaly Score"
        )

    with gr.Row():

        status_box = gr.Textbox(
            label="System Status"
        )

        agent_box = gr.Textbox(
            label="Agent Orchestration Status"
        )

    chart_output = gr.Plot(
        label="Live Operational Monitoring",
        min_width=1000,
        scale=2
    )

    with gr.Row():

        rag_box = gr.Textbox(
            label="Retrieved Maintenance Procedure",
            lines=6
        )

        recommendation_box = gr.Textbox(
            label="AI Recommendation",
            lines=6
        )

    run_button = gr.Button(
        "🚀 Run Monitoring Cycle"
    )
    hidden_mean = gr.Textbox(visible=False)
    hidden_std = gr.Textbox(visible=False)
    hidden_zscore = gr.Textbox(visible=False)
    hidden_roc = gr.Textbox(visible=False)
    hidden_slope = gr.Textbox(visible=False)
    run_button.click(
        fn=monitor_system,
        inputs=[],
        outputs=[
            chart_output,
            vibration_box,
            hidden_mean,
            hidden_std,
            hidden_zscore,
            hidden_roc,
            hidden_slope,
            prediction_box,
            anomaly_box,
            agent_box,
            status_box,
            rag_box,
            recommendation_box
        ]
    )
    timer = gr.Timer(5)

    timer.tick(
        fn=monitor_system,
        inputs=[],
        outputs=[
            chart_output,
            vibration_box,
            hidden_mean,
            hidden_std,
            hidden_zscore,
            hidden_roc,
            hidden_slope,
            prediction_box,
            anomaly_box,
            agent_box,
            status_box,
            rag_box,
            recommendation_box
        ]
    )

dashboard.launch(theme=gr.themes.Soft()
)