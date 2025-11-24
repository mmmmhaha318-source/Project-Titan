import os
import requests
import sys
import subprocess

def send_discord_notification(webhook_url, embed):
    if not webhook_url: return
    try:
        requests.post(webhook_url, json={"embeds": [embed]}).raise_for_status()
    except Exception as e:
        print(f"[ERR] Discord: {e}")

def get_ai_summary(findings_file, api_key):
    if not os.path.exists(findings_file) or os.path.getsize(findings_file) == 0:
        return "✅ No significant findings.", "ok"
    try:
        env = dict(os.environ, DEEPINFRA_API_TOKEN=api_key)
        result = subprocess.run(['python', 'core/ai_analyzer.py', findings_file], capture_output=True, text=True, check=True, env=env)
        return result.stdout.strip(), "critical" if "CRITICAL" in result.stdout else "high" if "HIGH" in result.stdout else "ok"
    except Exception as e:
        return f"AI analysis failed: {e}", "error"

def generate_report(target, summary, findings_file):
    try:
        subprocess.run(['python', 'core/pdf_generator.py', target, summary, findings_file], check=True)
    except Exception as e:
        print(f"Report generation failed: {e}")

if __name__ == "__main__":
    target = sys.argv[1]
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    api_key = os.getenv("DEEPINFRA_API_TOKEN")
        
    findings_path = f"results/{target}/vuln_scan/nuclei_findings.txt"
    summary, status = get_ai_summary(findings_path, api_key)
        
    color_map = {"critical": 0xff0000, "high": 0xffa500, "ok": 0x00ff00, "error": 0x808080}
        
    if status in ["critical", "high"]:
        generate_report(target, summary, findings_path)

    embed = {
        "title": f"⚔️ Titan AI Report: `{target}`",
        "description": f"**AI Summary:**\n```{summary}```",
        "color": color_map.get(status, 0x808080),
        "footer": {"text": f"Status: {status.upper()}"}
    }
    send_discord_notification(webhook, embed)
