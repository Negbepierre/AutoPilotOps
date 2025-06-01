from flask import Flask, jsonify
import random
import requests

app = Flask(__name__)

@app.route('/error-metrics', methods=['GET'])
def get_error_rate():
    error_rate = random.uniform(0, 1) * 100  # Simulate 0%–100% error rate
    error_rate = round(error_rate, 2)

    if error_rate > 20:
        action = {
            "service": "error_monitor",
            "proposal": "restart",
            "reason": f"High error rate detected: {error_rate}%"
        }
    else:
        action = {
            "service": "error_monitor",
            "proposal": "no_action",
            "reason": f"Error rate within acceptable limits: {error_rate}%"
        }

    try:
        res = requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"Submitted to coordinator: {res.status_code}")
    except Exception as e:
        print(f"Error sending to coordinator: {e}")

    return jsonify(action)

if __name__ == '__main__':
    app.run(port=5004)
