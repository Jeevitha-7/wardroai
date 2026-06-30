import os
import socket
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
VENV = ROOT / "backend" / ".venv"


def venv_python():
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def choose_port():
    for port in range(8501, 8511):
        if port_is_free(port):
            return port
    raise RuntimeError("No free Streamlit port found between 8501 and 8510.")


def main():
    python = venv_python()
    if not python.exists():
        print("Project environment is missing. Run `npm run setup` first.", file=sys.stderr)
        return 1

    port = choose_port()
    url = f"http://127.0.0.1:{port}"
    print(f"Starting WardroAI at {url}")

    command = [
        str(python),
        "-m",
        "streamlit",
        "run",
        str(APP),
        "--server.address",
        "127.0.0.1",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
