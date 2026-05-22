import ollama

# Simulated anomaly
anomaly = "High vibration detected in turbine."

# Retrieved maintenance document
retrieved_doc = """
High vibration levels may indicate bearing degradation.
Inspect bearings immediately.
"""

# Prompt sent to the local LLM
prompt = f"""
You are an industrial operations AI assistant.

Sensor anomaly:
{anomaly}

Maintenance procedure:
{retrieved_doc}

Generate a short operational recommendation.
"""

# Query local model
response = ollama.chat(
    model='mistral',
    messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ]
)

# Print generated response
print(response['message']['content'])