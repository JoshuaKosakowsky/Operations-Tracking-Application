"""Bounded local child-process lifecycle shared by startup checks."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
from urllib.error import URLError
from urllib.request import urlopen


@contextmanager
def running_server(root: Path, python: Path, logs: Path, *, launcher=False, env=None):
    logs.mkdir(parents=True, exist_ok=True)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    with (logs / "server.log").open("w", encoding="utf-8") as log:
        command = [str(python), "scripts/dev.py", "--port", str(port)] if launcher else [
            str(python), "-m", "uvicorn", "operations_tracking.app:app",
            "--host", "127.0.0.1", "--port", str(port),
        ]
        process = subprocess.Popen(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=os.name != "nt")
        try:
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"Server exited early; see {logs / 'server.log'}")
                try:
                    with urlopen(base + "/api/health", timeout=1) as response:
                        health = json.load(response)
                    if health.get("status") == "ok":
                        break
                except (URLError, TimeoutError, json.JSONDecodeError):
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("Server did not become healthy within 30 seconds")
            yield base
        finally:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            elif process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
