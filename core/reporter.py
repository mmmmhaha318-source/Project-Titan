import os
import requests
import sys

def send_discord_notification(webhook_url, message):
    if not webhook_url:
        print("[WARN] Discord webhook URL not set.")
        return
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("[INFO] Discord notification sent.")
    except Exception as e:
        print(f"[ERR] Failed to send Discord notification: {e}")

if __name__ == "__main__":
    target = sys.argv[1]
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
        
    message = f"✅ **Titan Hunt Completed:** Reconnaissance for `{target}` is finished."
        
    send_discord_notification(webhook, message)
