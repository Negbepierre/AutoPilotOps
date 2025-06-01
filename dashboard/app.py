from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        response = requests.get("http://localhost:5002/history")  # adjust if needed
        history = response.json()
    except Exception as e:
        history = []
        print("Failed to fetch history:", e)

    return render_template("dashboard.html", history=history)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
