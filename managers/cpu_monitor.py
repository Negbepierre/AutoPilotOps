from flask import Flask, jsonify
import random
import requests
import time
import threading

app = Flask(__name__)

# 🔁 Background worker
def send_cpu_metrics():
    while True:
        cpu_usage = random.randint(30, 95)

        action = {
            "service": "cpu_monitor",
            "proposal": "scale_up" if cpu_usage > 80 else "no_action",
            "reason": f"CPU usage {'high' if cpu_usage > 80 else 'normal'}: {cpu_usage}%"
        }

        try:
            requests.post("http://localhost:5002/submit-proposal", json=action)
            print(f"[AUTO] Sent proposal: {action}")
        except Exception as e:
            print("[AUTO] Failed to send:", e)

        time.sleep(10)  # wait 10 seconds before sending next

# 🧪 Manual trigger via browser or Postman
@app.route('/cpu-metrics', methods=['GET'])
def get_cpu_status():
    cpu_usage = random.randint(30, 95)

    action = {
        "service": "cpu_monitor",
        "proposal": "scale_up" if cpu_usage > 80 else "no_action",
        "reason": f"CPU usage {'high' if cpu_usage > 80 else 'normal'}: {cpu_usage}%"
    }

    try:
        requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"[MANUAL] Sent proposal: {action}")
    except Exception as e:
        print("[MANUAL] Failed to send:", e)

    return jsonify(action)

if __name__ == '__main__':
    # 🧵 Start auto-submission in a background thread
    threading.Thread(target=send_cpu_metrics, daemon=True).start()

    # 🌍 Start Flask server for manual interaction
    app.run(port=5001, host="0.0.0.0")
