from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        response = requests.get("http://localhost:5002/history")
        history = response.json()
    except Exception as e:
        history = []
        print("Failed to fetch history:", e)

    return render_template("dashboard.html", history=history)

if __name__ == '__main__':
    app.run(port=5005)
