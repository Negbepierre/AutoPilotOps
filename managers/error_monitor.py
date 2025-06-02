from flask import Flask, jsonify
import requests
import time
import random
import threading

app = Flask(__name__)

def send_error_metrics():
    while True:
        error_rate = round(random.uniform(0, 1), 2)

        action = {
            "service": "error_monitor",
            "proposal": "restart" if error_rate > 0.7 else "no_action",
            "reason": f"Error rate {'critical' if error_rate > 0.7 else 'normal'}: {error_rate}"
        }

        try:
            requests.post("http://localhost:5002/submit-proposal", json=action)
            print(f"[AUTO] Sent proposal: {action}")
        except Exception as e:
            print("[AUTO] Failed to send:", e)

        time.sleep(10)

@app.route('/error-metrics', methods=['GET'])
def get_error_status():
    error_rate = round(random.uniform(0, 1), 2)

    action = {
        "service": "error_monitor",
        "proposal": "restart" if error_rate > 0.7 else "no_action",
        "reason": f"Error rate {'critical' if error_rate > 0.7 else 'normal'}: {error_rate}"
    }

    try:
        requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"[MANUAL] Sent proposal: {action}")
    except Exception as e:
        print("[MANUAL] Failed to send:", e)

    return jsonify(action)

if __name__ == '__main__':
    threading.Thread(target=send_error_metrics, daemon=True).start()
    app.run(port=5004, host="0.0.0.0")
