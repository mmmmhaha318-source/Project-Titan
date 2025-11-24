import os
import sys
import requests

LLM_API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def analyze_findings(findings_text, api_key):
    if not findings_text.strip():
        return "No vulnerabilities found.", "ok"

    if not api_key:
        return "AI analysis skipped: API key not configured.", "warning"

    prompt = f"""
    Analyze the following Nuclei scan results and provide a very brief, one-line summary for a bug bounty hunter.
    Focus only on high or critical severity findings. Ignore informational or low-severity ones.
    If there are critical findings, start the summary with "🚨 CRITICAL:".
    If there are high severity findings, start with "🔥 HIGH:".
    If nothing significant is found, say "✅ No significant findings."

    Results:
    ---
    {findings_text}
    ---
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content'].strip()
        if "CRITICAL" in summary:
            return summary, "critical"
        elif "HIGH" in summary:
            return summary, "high"
        else:
            return summary, "ok"
    except Exception as e:
        return f"AI analysis failed: {e}", "error"

if __name__ == "__main__":
    file_path = sys.argv[1]
    api_key = os.getenv("DEEPINFRA_API_TOKEN")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        summary, _ = analyze_findings(content, api_key)
        print(summary)
    except FileNotFoundError:
        print("No findings file found.")
