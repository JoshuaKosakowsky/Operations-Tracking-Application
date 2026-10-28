"""Audit exact locked packages for this platform; never update dependencies."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    output = ROOT / "results" / "audit"
    output.mkdir(parents=True, exist_ok=True)
    requirements = output / "requirements.txt"
    subprocess.run([
        "uv", "export", "--locked", "--all-groups", "--no-emit-project",
        "--format", "requirements-txt", "--output-file", str(requirements),
    ], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Keep the audit tool itself locked. Hashed exported pins prevent resolving
    # a different set; markers select this runner's platform.
    subprocess.run([
        "uv", "run", "--locked", "--group", "audit", "pip-audit",
        "--strict", "--require-hashes", "--disable-pip", "--progress-spinner", "off",
        "-r", str(requirements), "--format", "json", "--output", str(output / "report.json"),
    ], cwd=ROOT, check=True)
    print("Locked dependency vulnerability audit passed for this platform.")


if __name__ == "__main__":
    main()
