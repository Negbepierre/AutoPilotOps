from flask import Flask, jsonify
import random
import requests

app = Flask(__name__)

@app.route('/memory-metrics', methods=['GET'])
def get_memory_status():
    memory_usage = random.randint(40, 95)

    if memory_usage > 85:
        action = {
            "service": "memory_monitor",
            "proposal": "scale_up",
            "reason": f"Memory usage high: {memory_usage}%"
        }
    else:
        action = {
            "service": "memory_monitor",
            "proposal": "no_action",
            "reason": f"Memory usage normal: {memory_usage}%"
        }

    try:
        res = requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"Submitted to coordinator: {res.status_code}")
    except Exception as e:
        print(f"Error sending to coordinator: {e}")

    return jsonify(action)

if __name__ == '__main__':
    app.run(port=5003)
