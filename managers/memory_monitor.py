from flask import Flask, jsonify
import psutil
import requests
import time
import threading

app = Flask(__name__)

def send_memory_metrics():
    while True:
        memory_usage = psutil.virtual_memory().percent

        action = {
            "service": "memory_monitor",
            "proposal": "scale_up" if memory_usage > 75 else "no_action",
            "reason": f"Memory usage {'high' if memory_usage > 75 else 'normal'}: {memory_usage}%"
        }

        try:
            requests.post("http://localhost:5002/submit-proposal", json=action)
            print(f"[AUTO] Sent proposal: {action}")
        except Exception as e:
            print("[AUTO] Failed to send:", e)

        time.sleep(10)

@app.route('/memory-metrics', methods=['GET'])
def get_memory_status():
    memory_usage = psutil.virtual_memory().percent

    action = {
        "service": "memory_monitor",
        "proposal": "scale_up" if memory_usage > 75 else "no_action",
        "reason": f"Memory usage {'high' if memory_usage > 75 else 'normal'}: {memory_usage}%"
    }

    try:
        requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"[MANUAL] Sent proposal: {action}")
    except Exception as e:
        print("[MANUAL] Failed to send:", e)

    return jsonify(action)

if __name__ == '__main__':
    threading.Thread(target=send_memory_metrics, daemon=True).start()
    app.run(port=5003, host="0.0.0.0")
