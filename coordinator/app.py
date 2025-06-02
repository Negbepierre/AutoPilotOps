from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

@app.route('/submit-proposal', methods=['POST'])
def submit_proposal():
    data = request.get_json()
    print("Received:", data)
    return jsonify({"status": "received", "data": data}), 200

@app.route('/decide', methods=['GET'])
def decide():
    return jsonify({
        "final_decision": "scale_up",
        "details": [
            {
                "service": "cpu_monitor",
                "proposal": "scale_up",
                "reason": "CPU usage reached 92%"
            }
        ]
    })

@app.route('/history', methods=['GET'])
def get_history():
    # Mocked response (no Redis)
    return jsonify([
        {
            "timestamp": "2025-06-02 11:00:00",
            "decision": "scale_up",
            "proposals": [
                {"service": "cpu_monitor", "proposal": "scale_up", "reason": "CPU at 91%"}
            ]
        },
        {
            "timestamp": "2025-06-02 10:55:00",
            "decision": "no_action",
            "proposals": []
        }
    ])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
