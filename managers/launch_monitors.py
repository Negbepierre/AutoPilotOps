import subprocess
import time
import sys
import os

def launch_all():
    # Use the current venv’s Python interpreter
    python_executable = sys.executable

    services = [
        "cpu_monitor.py",
        "memory_monitor.py",
        "error_monitor.py"
    ]

    processes = []
    for script in services:
        print(f"Starting {script}...")
        proc = subprocess.Popen(
            [python_executable, script],
            cwd=os.path.join(os.getcwd(), "managers")
        )
        processes.append(proc)
        time.sleep(1)

    print("✅ All monitors are running. Press CTRL+C to stop.")

    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\nStopping monitors...")
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    launch_all()
