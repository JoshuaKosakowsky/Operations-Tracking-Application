"""Check skeleton inventory and prevent common private files entering Git."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md", "CONTRIBUTING.md", "PLAN.md", "README.md", "handoff.md",
    ".gitignore", ".gitattributes", ".python-version", ".env.example", "pyproject.toml", "uv.lock",
    "docs/TESTING.md", "docs/TEST_RESULTS.md", "docs/GITHUB_SETUP.md", "docs/INTEGRATIONS.md",
    "docs/COMMITS.md", "docs/CONTRIBUTIONS.md", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.md", ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/workflows/ci.yml", ".github/workflows/security.yml",
    "operations_tracking/app.py", "operations_tracking/static/index.html",
    "operations_tracking/static/status.js", "scripts/dev.py", "scripts/browser_smoke.py",
    "scripts/source_zip_check.py", "scripts/audit.py", "tests/test_app.py",
)


def private_path(name: str) -> bool:
    path = Path(name)
    parts = set(path.parts)
    filename = path.name.lower()
    return bool(parts & {".venv", "__pycache__", "data", "uploads", "secrets", "results"}) or (
        filename == ".env" or (filename.startswith(".env.") and filename != ".env.example")
        or (filename.endswith(".json") and filename.startswith(("credentials", "client_secret", "token")))
        or path.suffix.lower() in {".pem", ".key", ".db", ".sqlite", ".zip"}
    )


def main() -> None:
    problems = [f"Missing: {name}" for name in REQUIRED if not (ROOT / name).is_file()]
    if (ROOT / ".git").exists():
        tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        problems.extend(f"Private/generated path tracked: {name}" for name in tracked if name and private_path(name))
    if problems:
        raise SystemExit("\n".join(problems))
    print("Repository inventory and tracked-path safeguards passed (not a full secret scan).")


if __name__ == "__main__":
    main()
