import os
import httpx
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_maintenance_report(
    prediction_result: dict,
    vehicle_type: str,
    vehicle_age: float,
    total_kilometers: float,
    vehicle_name: str,
    model: str
) -> str:
    """
    Generates a detailed maintenance report using Groq AI based on prediction results.
    If the API key is not configured, it returns a locally generated mock report.
    """
    
    # Construct a prompt describing the vehicle and the prediction result
    prompt = f"""
You are an expert vehicle maintenance AI. Generate a detailed, professional maintenance report for the following vehicle based on the provided diagnostic data:

Vehicle Info:
- Name: {vehicle_name}
- Model: {model}
- Type: {vehicle_type} (L=Low quality, M=Medium quality)
- Age: {vehicle_age} years
- Total Kilometers: {total_kilometers} km

Diagnostic Result:
- Failure Detected: {'Yes' if prediction_result.get('failure') == 1 else 'No'}
- Probability of Failure: {prediction_result.get('failure_probability', 0)}
- Failure Types: {prediction_result.get('failure_types', 'None')}

Please provide a Markdown formatted report with the following sections (Use strictly # and ## for headers, avoid using ==== underlines for headers):
1. Executive Summary
2. Diagnostic Analysis (explain what the failure types mean, if any)
3. Recommended Immediate Actions
4. Long-term Maintenance Strategy
"""

    if not GROQ_API_KEY:
        # Fallback if no API key is provided
        fallback_msg = f"""# Vehicle Maintenance Report: {vehicle_name} ({model})

*Note: This is an auto-generated summary because the Groq AI API key is not configured.*

## Executive Summary
The diagnostic system has analyzed the vehicle data. 
**Failure Detected:** {'Yes' if prediction_result.get('failure') == 1 else 'No'}
**Probability:** {prediction_result.get('failure_probability', 0)}

## Diagnostic Analysis
**Failure Types:** {prediction_result.get('failure_types', 'None')}

## Recommended Actions
Please inspect the machine according to standard maintenance protocols for the indicated failure types.
"""
        return fallback_msg

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",  # Updated from deprecated model
        "messages": [
            {"role": "system", "content": "You are a helpful and expert vehicle maintenance analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            report = data['choices'][0]['message']['content']
            return report
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return f"An error occurred while generating the AI report: {str(e)}\n\nRaw prediction: {json.dumps(prediction_result, indent=2)}"
