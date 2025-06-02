from flask import Flask, jsonify
import threading
import random
import requests
import time

app = Flask(__name__)

def submit_cpu_metrics():
    while True:
        cpu_usage = random.randint(30, 95)
        if cpu_usage > 80:
            data = {
                "service": "cpu_monitor",
                "proposal": "scale_up",
                "reason": f"CPU usage high: {cpu_usage}%"
            }
        else:
            data = {
                "service": "cpu_monitor",
                "proposal": "no_action",
                "reason": f"CPU usage normal: {cpu_usage}%"
            }
        try:
            res = requests.post("http://localhost:5002/submit-proposal", json=data)
            print(f"[CPU] Sent to coordinator: {res.status_code}")
        except Exception as e:
            print(f"[CPU] Error: {e}")
        time.sleep(10)

@app.route('/cpu-metrics', methods=['GET'])
def cpu_status():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    threading.Thread(target=submit_cpu_metrics).start()
    app.run(port=5001)
