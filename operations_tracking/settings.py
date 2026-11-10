"""Small, server-only configuration shared by local and hosted runs."""

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def build_id() -> str:
    supplied = os.getenv("RENDER_GIT_COMMIT") or os.getenv("BUILD_SHA")
    archive = ROOT / "operations_tracking" / "build.txt"
    if not supplied and archive.exists():
        supplied = archive.read_text().strip()
    if supplied and re.fullmatch(r"[0-9a-f]{40}", supplied):
        return supplied
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL, timeout=2,
        ).decode().strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, stderr=subprocess.DEVNULL, timeout=2,
        ).strip()
        return sha + ("-modified" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        return "development-unidentified"


@dataclass(frozen=True)
class Settings:
    database_url: str
    access_code: str = ""
    production: bool = False
    origin: str = ""
    build: str = "test-build"

    @classmethod
    def load(cls):
        load_dotenv(ROOT / ".env", override=False)
        production = os.getenv("APP_ENV", "local") == "production"
        database = os.getenv("DATABASE_URL", "")
        if not database:
            if production:
                raise ValueError("Hosted deployment requires a durable DATABASE_URL.")
            (ROOT / "data").mkdir(exist_ok=True)
            database = "sqlite:///" + (ROOT / "data" / "operations.db").as_posix()
        if database.startswith("postgresql://"):
            database = database.replace("postgresql://", "postgresql+psycopg://", 1)
        code = os.getenv("TEAM_ACCESS_CODE", "")
        origin = os.getenv("APP_ORIGIN", "").rstrip("/")
        if production:
            parsed = urlparse(origin)
            if len(code) < 24 or parsed.scheme != "https" or not parsed.hostname:
                raise ValueError("Hosting requires TEAM_ACCESS_CODE (24+ characters) and HTTPS APP_ORIGIN.")
            if not database.startswith("postgresql+psycopg://"):
                raise ValueError("Hosting requires PostgreSQL; local files do not survive free-host restarts.")
        return cls(database, code, production, origin, build_id())
