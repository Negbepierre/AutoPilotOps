from flask import Flask, jsonify
import threading
import random
import requests
import time

app = Flask(__name__)

def submit_error_metrics():
    while True:
        error_rate = random.random()
        if error_rate > 0.6:
            data = {
                "service": "error_monitor",
                "proposal": "restart",
                "reason": f"Error rate too high: {round(error_rate, 2)}"
            }
        else:
            data = {
                "service": "error_monitor",
                "proposal": "no_action",
                "reason": f"Error rate acceptable: {round(error_rate, 2)}"
            }
        try:
            res = requests.post("http://localhost:5002/submit-proposal", json=data)
            print(f"[Error] Sent to coordinator: {res.status_code}")
        except Exception as e:
            print(f"[Error] Error: {e}")
        time.sleep(15)

@app.route('/error-metrics', methods=['GET'])
def error_status():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    threading.Thread(target=submit_error_metrics).start()
    app.run(port=5004)
