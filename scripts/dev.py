"""One-command locked startup/checks, including long Windows checkout paths."""

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def environment() -> dict[str, str]:
    env = os.environ.copy()
    env["UV_LINK_MODE"] = "copy"
    if os.name == "nt" and "UV_PROJECT_ENVIRONMENT" not in env:
        identity = hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
        base = Path(env.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        env["UV_PROJECT_ENVIRONMENT"] = str(base / "OTA" / identity)
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    uv = shutil.which("uv")
    if uv is None:
        parser.exit(1, "Install uv first: python -m pip install uv==0.12.19\n")
    env = environment()
    base = [uv, "run", "--locked"]
    commands = [
        [*base, "python", "scripts/verify_repo.py"],
        [*base, "ruff", "check", "."],
        [*base, "pytest"],
    ] if args.check else [[
        *base, "--no-dev", "python", "-m", "uvicorn", "operations_tracking.app:app",
        "--host", "127.0.0.1", "--port", str(args.port),
    ]]
    try:
        for command in commands:
            subprocess.run(command, cwd=ROOT, env=env, check=True)
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
