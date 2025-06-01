from flask import Flask, jsonify
import random
import requests  # ✅ Add this

app = Flask(__name__)

@app.route('/cpu-metrics', methods=['GET'])
def get_cpu_status():
    cpu_usage = random.randint(30, 95)
    
    if cpu_usage > 80:
        action = {
            "service": "cpu_monitor",
            "proposal": "scale_up",
            "reason": f"CPU usage high: {cpu_usage}%"
        }
    else:
        action = {
            "service": "cpu_monitor",
            "proposal": "no_action",
            "reason": f"CPU usage normal: {cpu_usage}%"
        }

    # ✅ Send proposal to coordinator
    try:
        res = requests.post("http://localhost:5002/submit-proposal", json=action)
        print(f"Submitted to coordinator: {res.status_code}")
    except Exception as e:
        print(f"Error sending to coordinator: {e}")

    return jsonify(action)

if __name__ == '__main__':
    app.run(port=5001)
