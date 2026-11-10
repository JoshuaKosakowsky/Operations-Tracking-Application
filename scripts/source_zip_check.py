"""Validate an exact GitHub source archive in a clean, independent installation."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.request import Request, urlopen
import zipfile

from startup_support import running_server
from verify_repo import private_path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--repository", default="JoshuaKosakowsky/Operations-Tracking-Application")
    parser.add_argument("--archive", type=Path, help="Local git-archive rehearsal only; not GitHub proof")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.sha):
        parser.error("sha must be a full lowercase 40-character commit SHA")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository):
        parser.error("repository must be owner/name")
    artifacts = ROOT / "results" / "source-zip"
    artifacts.mkdir(parents=True, exist_ok=True)
    url = f"https://api.github.com/repos/{args.repository}/zipball/{args.sha}"
    archive = artifacts / "source.zip"
    if args.archive:
        archive.write_bytes(args.archive.read_bytes())
    else:
        with urlopen(url, timeout=120) as response:
            archive.write_bytes(response.read())
    with tempfile.TemporaryDirectory(prefix="ota-zip-") as temporary:
        clean = Path(temporary)
        with zipfile.ZipFile(archive) as source:
            names = [PurePosixPath(name) for name in source.namelist()]
            roots = {path.parts[0] for path in names if path.parts}
            if len(roots) != 1:
                raise RuntimeError("Archive must have exactly one top-level directory")
            for path in names:
                relative = Path(*path.parts[1:])
                if path.is_absolute() or ".." in path.parts or "\\" in str(path) or ":" in str(path):
                    raise RuntimeError("Unsafe archive member")
                if ".git" in path.parts or private_path(str(relative)):
                    raise RuntimeError(f"Forbidden archive member: {relative}")
            source.extractall(clean)
        project = clean / roots.pop()
        env = os.environ.copy()
        # An isolated environment must not reuse a developer's installed packages,
        # PYTHONPATH, project configuration or credentials.
        for key in list(env):
            if key.startswith(("OPENAI_", "GOOGLE_", "UV_", "APP_", "TEAM_", "AI_")) or key in {"VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME", "DATABASE_URL", "RENDER_GIT_COMMIT", "BUILD_SHA"}:
                env.pop(key, None)
        env["UV_PROJECT_ENVIRONMENT"] = str(clean / "runtime")
        env["UV_LINK_MODE"] = "copy"
        subprocess.run(["uv", "sync", "--locked", "--no-dev", "--python", "3.12"], cwd=project, env=env, check=True, timeout=180)
        python = clean / "runtime" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        # The exact same launcher documented in README must work from the ZIP.
        with running_server(project, python, artifacts, launcher=True, env=env) as base:
            with urlopen(base, timeout=5) as response:
                html = response.read().decode()
            with urlopen(base + "/assets/status.js", timeout=5) as response:
                javascript = response.read().decode()
            if "Operations Tracking Application" not in html or "/api/session" not in javascript:
                raise RuntimeError("Archive startup page or static asset missing")
            with urlopen(base + "/api/health", timeout=5) as response:
                actual = json.load(response)
            if actual["build"] != args.sha:
                raise RuntimeError("Running archive build does not match the requested commit")
            body = {"day":"2026-11-10", "time":"08:00", "title":"Clean ZIP example",
                    "site":"Fictional site", "crew":"Example crew", "site_minutes":60, "modules":4}
            request = Request(base + "/api/jobs", data=json.dumps(body).encode(),
                              headers={"Content-Type":"application/json", "X-OTA-Request":"1"}, method="POST")
            with urlopen(request, timeout=5) as response:
                if response.status != 201:
                    raise RuntimeError("Clean ZIP could not save a job")
            with urlopen(base + "/api/report?day=2026-11-10", timeout=5) as response:
                report = json.load(response)
            if report["totals"]["modules"] != 4 or report["totals"]["modules_per_site_hour"] != 4:
                raise RuntimeError("Clean ZIP did not produce the expected report")
        record = {
            "sha": args.sha,
            "archive_url": url if not args.archive else None,
            "source": "GitHub exact-commit archive" if not args.archive else "local rehearsal only",
            "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "git_metadata": False, "dotenv": False, "isolated_runtime": True,
            "startup": "passed", "home_and_static_assets": "passed",
            "running_build_matches": True, "save_and_report": "passed",
        }
        (artifacts / "record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
