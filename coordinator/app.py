from flask import Flask, request, jsonify
import redis
import json
import time

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# --- 1. Submit proposal ---
@app.route('/submit-proposal', methods=['POST'])
def submit_proposal():
    data = request.get_json()
    key = f"proposal:{data['service']}"
    r.set(key, json.dumps(data))
    return jsonify({"status": "received", "data": data})


# --- 2. Resolve decisions and store history ---
@app.route('/decide', methods=['GET'])
def decide():
    proposals = []
    for key in r.scan_iter("proposal:*"):
        proposals.append(json.loads(r.get(key)))
        r.delete(key)

    # Simple logic: scale_up or restart means 'take action'
    action_votes = [p for p in proposals if p['proposal'] in ('scale_up', 'restart')]
    final_decision = "scale_up" if action_votes else "no_action"

    # Store decision history
    decision_record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "decision": final_decision,
        "proposals": proposals
    }

    history_key = f"history:{int(time.time())}"
    r.set(history_key, json.dumps(decision_record))

    return jsonify({
        "final_decision": final_decision,
        "details": proposals
    })


# --- 3. View stored decision history ---
@app.route('/history', methods=['GET'])
def get_history():
    history_items = []
    for key in sorted(r.scan_iter("history:*")):
        value = r.get(key)
        if value:
            history_items.append(json.loads(value))
    return jsonify(history_items)


if __name__ == '__main__':
    app.run(port=5002)
