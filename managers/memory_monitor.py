from flask import Flask, jsonify
import threading
import random
import requests
import time

app = Flask(__name__)

def submit_memory_metrics():
    while True:
        mem_usage = random.randint(40, 95)
        if mem_usage > 85:
            data = {
                "service": "memory_monitor",
                "proposal": "restart",
                "reason": f"Memory usage critical: {mem_usage}%"
            }
        else:
            data = {
                "service": "memory_monitor",
                "proposal": "no_action",
                "reason": f"Memory usage stable: {mem_usage}%"
            }
        try:
            res = requests.post("http://localhost:5002/submit-proposal", json=data)
            print(f"[Memory] Sent to coordinator: {res.status_code}")
        except Exception as e:
            print(f"[Memory] Error: {e}")
        time.sleep(12)

@app.route('/memory-metrics', methods=['GET'])
def memory_status():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    threading.Thread(target=submit_memory_metrics).start()
    app.run(port=5003)
