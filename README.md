
# 🧠 AutoPilotOps

AutoPilotOps is a lightweight, event-driven observability and automation framework. It simulates system monitors (CPU, Memory, Error Rate) that make proposals to a decision coordinator, which decides when to trigger scaling or recovery actions. All decisions are viewable in a real-time dashboard.

---

## 🔧 Project Structure

AutoPilotOps/
│
├── coordinator/ # Central service that receives proposals and makes decisions
│ └── app.py
│
├── dashboard/ # Frontend that displays decision history
│ ├── app.py
│ └── templates/
│ └── dashboard.html
│
├── managers/ # Simulated system monitors (send proposals)
│ ├── cpu_monitor.py
│ ├── memory_monitor.py
│ ├── error_monitor.py
│ └── launch_monitors.py # Launch all monitors using threads
│
├── venv/ # Python virtual environment (not pushed to GitHub)
├── requirements.txt # Python dependencies
└── README.md


---

## 🌐 Live Demo

- **Dashboard UI:** https://autopilotops-dashboard.onrender.com
- **Coordinator API:** https://autopilotops-coordinator.onrender.com

---

## 🚀 Features

✅ Simulated monitors for CPU, memory, and error rate  
✅ Coordinator that aggregates and decides on actions  
✅ Persistent or mocked decision history  
✅ Real-time HTML dashboard to visualize decision data  
✅ Deployable on **Render** (no Redis mode supported)

---

## ⚙️ How It Works

- Each monitor sends proposals to the coordinator via `/submit-proposal`
- Coordinator receives and logs decisions via `/decide`
- Dashboard calls `/history` and renders all decisions using Flask + Jinja2

---

## 💻 Local Development

### 1. Clone the repo

```bash
git clone https://github.com/Negbepierre/AutoPilotOps.git
cd AutoPilotOps


2. Set up virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt

3. Run each service
In 3 separate terminals:
# Terminal 1 - Coordinator
python coordinator/app.py

# Terminal 2 - Dashboard
python dashboard/app.py

# Terminal 3 - Launch Monitors
python managers/launch_monitors.py

☁️ Deployment on Render
Deploy coordinator/app.py as a web service (Python, Flask, port 5002)

Deploy dashboard/app.py as a separate service (port 5005 or default)

You can use mocked history (no Redis) for easier deployment
