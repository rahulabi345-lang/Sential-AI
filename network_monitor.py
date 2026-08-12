import psutil
import json
import time
import requests
from datetime import datetime

print("Sentinel AI Network Monitor Started")
print("-" * 50)

known_connections = set()

while True:

    connections = psutil.net_connections()

    current_connections = set()

    for connection in connections:

        if connection.status == "ESTABLISHED" and connection.pid:

            connection_id = (
                connection.pid,
                connection.laddr,
                connection.raddr
            )

            current_connections.add(connection_id)

            if connection_id not in known_connections:

                try:
                    process = psutil.Process(connection.pid)

                    process_name = process.name().lower()

                    if process_name in ["python.exe", "uvicorn.exe"]:
                        classification = "sentinel_related"

                    elif process_name in [
    "svchost.exe",
    "system",
    "services.exe"
]:
                        classification = "system"

                    else:
                        classification = "unknown"

                    event = {
    "event_type": "network_connection",
    "timestamp": datetime.now().isoformat(),
    "process_name": process.name(),
    "pid": connection.pid,
    "path": process.exe(),
    "username": process.username(),

    "details": {
        "local_ip": connection.laddr.ip,
        "local_port": connection.laddr.port,
        "remote_ip": connection.raddr.ip,
        "remote_port": connection.raddr.port,
        "status": connection.status,
        "classification": classification,
    }
}

                    print("[NEW NETWORK CONNECTION]")
                    print(json.dumps(event, indent=4))
                    print("-" * 50)

                    response = requests.post(
    "http://127.0.0.1:8000/events",
    json=event
)

                    print("Backend response:", response.json())

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    known_connections = current_connections

    time.sleep(2)