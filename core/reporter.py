import os
import requests
import sys
import subprocess

def send_discord_notification(webhook_url, embed):
    if not webhook_url:
        print("[WARN] Discord webhook URL not set.")
        return
    try:
        requests.post(webhook_url, json={"embeds": [embed]}).raise_for_status()
        print("[INFO] Discord notification sent.")
    except Exception as e:
        print(f"[ERR] Failed to send Discord notification: {e}")

def get_ai_summary(findings_file, api_key):
    if not os.path.exists(findings_file):
        return "No findings file.", "info"
    try:
        result = subprocess.run(
            ['python', 'core/ai_analyzer.py', findings_file],
            capture_output=True, text=True, check=True, env=dict(os.environ, DEEPINFRA_API_TOKEN=api_key)
        )
        summary = result.stdout.strip()
        if "CRITICAL" in summary: return summary, 0xff0000 # Red
        if "HIGH" in summary: return summary, 0xffa500 # Orange
        return summary, 0x00ff00 # Green
    except Exception as e:
        return f"AI analysis failed: {e}", 0x808080 # Grey

if __name__ == "__main__":
    target = sys.argv[1]
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    api_key = os.getenv("DEEPINFRA_API_TOKEN")
        
    findings_path = f"results/{target}/vuln_scan/nuclei_findings.txt"
    summary, color = get_ai_summary(findings_path, api_key)

    embed = {
        "title": f"⚔️ Titan AI Report: `{target}`",
        "description": f"**AI Summary:**\n```{summary}```",
        "color": color
    }
    send_discord_notification(webhook, embed)
