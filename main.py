import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import ollama
import time
import random
# =========================================
# =========================================
# =========================================
# SENSOR AGENT
# =========================================

print("=== SENSOR AGENT ===")

# Initial sensor readings
vibration_history = [0.20, 0.21, 0.22, 0.23, 0.24]

# Rolling window size
window_size = 5

anomaly_detected = False

# Simulate live sensor stream
for i in range(15):

    # Generate mostly normal values
    new_value = random.uniform(0.20, 0.25)

    # Inject anomaly
    if i == 10:
        new_value = 0.90

    print(f"\nIncoming vibration reading: {new_value:.2f}")

    # Extract rolling window
    rolling_window = vibration_history[-window_size:]

    # Compute rolling statistics
    mean = np.mean(rolling_window)
    std = np.std(rolling_window)

    # Avoid division by zero
    if std == 0:
        std = 0.0001

    # Compute z-score
    z_score = (new_value - mean) / std
    # Compute rate of change
    previous_value = vibration_history[-1]
    rate_of_change = new_value - previous_value

    print(f"Rate of Change: {rate_of_change:.2f}")
    # Compute trend slope using rolling window
    x = np.arange(len(rolling_window))
    slope, intercept = np.polyfit(x, rolling_window, 1)

    print(f"Trend Slope: {slope:.4f}")
    print(f"Rolling Mean: {mean:.2f}")
    print(f"Rolling Std Dev: {std:.4f}")
    print(f"Z-score: {z_score:.2f}")

    # Detect anomaly
    threshold = 3

    roc_threshold = 0.30
    trend_threshold = 0.02

    # Initialize anomaly score
    anomaly_score = 0

    # Statistical anomaly
    if abs(z_score) > threshold:
        anomaly_score += 1

    # Sudden signal jump
    if abs(rate_of_change) > roc_threshold:
       anomaly_score += 1

    # Progressive upward degradation
    if slope > trend_threshold:
        anomaly_score += 1

    print(f"Anomaly Score: {anomaly_score}")

    # Final anomaly decision
    if anomaly_score >= 2:

        anomaly_detected = True
        anomaly_text = "Critical turbine vibration anomaly detected."

        print("ALERT:", anomaly_text)

        vibration_history.append(new_value)

        break

    else:
        print("System operating normally.")

    # Update history
    vibration_history.append(new_value)

    # Simulate real-time streaming delay
    time.sleep(1)

# =========================================
# RAG AGENT
# =========================================

if anomaly_detected:

    print("\n=== RAG AGENT ===")

    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load maintenance docs
    with open("data/manuals.txt", "r") as file:
        documents = file.read().split("\n\n")

    # Create embeddings
    doc_embeddings = model.encode(documents)

    # Create FAISS index
    dimension = doc_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings
    index.add(np.array(doc_embeddings))

    # Encode anomaly query
    query_embedding = model.encode([anomaly_text])

    # Search
    k = 1
    distances, indices = index.search(np.array(query_embedding), k)

    # Retrieve best doc
    retrieved_doc = documents[indices[0][0]]

    print("Retrieved Procedure:")
    print(retrieved_doc)

    # =========================================
    # LLM AGENT
    # =========================================

    print("\n=== LLM RECOMMENDATION AGENT ===")

    prompt = f"""
    You are an industrial operations AI assistant.

    Sensor anomaly:
    {anomaly_text}

    Maintenance procedure:
    {retrieved_doc}

    Generate a short operational recommendation.
    """

    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    recommendation = response['message']['content']

    print("AI Recommendation:")
    print(recommendation)