import json
import requests
import psutil
import time
import socket
from datetime import datetime

print("Sentinel AI Monitor Started")
print("-" * 50)

# Get the processes that are already running
known_processes = set()

for process in psutil.process_iter(["pid"]):
    known_processes.add(process.info["pid"])

print(f"Monitoring {len(known_processes)} processes...")
print("-" * 50)

# Keep monitoring continuously
while True:

    current_processes = set()

    for process in psutil.process_iter(["pid"]):
        current_processes.add(process.info["pid"])

    # Find newly started processes
    new_processes = current_processes - known_processes

    for pid in new_processes:

        try:
            process = psutil.Process(pid)

              # Basic process classification
            if process.name().lower() in [
        "python.exe",
        "uvicorn.exe"
    ]:
                process_name_lower = process.name().lower()

            sentinel_processes = [
                "python.exe",
                "uvicorn.exe"
            ]

            system_processes = [
                "svchost.exe",
                "explorer.exe",
                "searchfilterhost.exe",
                "backgroundtaskhost.exe",
                "services.exe",
                "lsass.exe",
                "wininit.exe",
                "winlogon.exe"
            ]

            suspicious_processes = [
                "powershell.exe",
                "cmd.exe",
                "wscript.exe",
                "cscript.exe"
            ]

            if process_name_lower in sentinel_processes:
                classification = "sentinel_related"
                severity = "low"

            elif process_name_lower in system_processes:
                classification = "system"
                severity = "low"

            elif process_name_lower in suspicious_processes:
                classification = "suspicious"
                severity = "high"

            else:
                classification = "unknown"
                severity = "low"

            # Get parent process
            parent = process.parent()

            if parent:
                parent_pid = parent.pid
                parent_process = parent.name()
            else:
                parent_pid = None
                parent_process = None

            # Get command line
            try:
                command_line = process.cmdline()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                command_line = []

            event = {
    "timestamp": datetime.now().isoformat(),
    "event_type": "process_start",
    "source": "windows_process_monitor",
    "hostname": socket.gethostname(),
    "username": process.username(),
    "process_name": process.name(),
    "process_id": process.pid,
    "severity": "low",
    "description": f"New process detected: {process.name()}",
    "raw_data": {
        "path": process.exe(),
        "parent_pid": parent_pid,
        "parent_process": parent_process,
        "command_line": command_line,
        "classification": classification
    }
}

            print("[NEW PROCESS DETECTED]")
            print(json.dumps(event, indent=4))
            print("-" * 50)

            response = requests.post(
    "http://127.0.0.1:8000/events",
    json=event,
    timeout=5
)

            print("Backend response:", response.json())

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    known_processes = current_processes

    time.sleep(2)