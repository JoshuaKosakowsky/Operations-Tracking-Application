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
    ai_base_url: str = ""
    ai_model: str = ""
    ai_api_key: str = ""

    @property
    def ai_available(self):
        return bool(self.ai_base_url and self.ai_model and self.ai_api_key)

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
        origin = (os.getenv("APP_ORIGIN") or os.getenv("RENDER_EXTERNAL_URL", "")).rstrip("/")
        if production:
            parsed = urlparse(origin)
            if (len(code) < 24 or parsed.scheme != "https" or not parsed.hostname
                    or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment):
                raise ValueError("Hosting requires TEAM_ACCESS_CODE (24+ characters) and HTTPS APP_ORIGIN.")
            if not database.startswith("postgresql+psycopg://"):
                raise ValueError("Hosting requires PostgreSQL; local files do not survive free-host restarts.")
        ai_url = os.getenv("AI_BASE_URL", "").rstrip("/")
        ai_model = os.getenv("AI_MODEL", "")
        ai_key = os.getenv("AI_API_KEY", "")
        if any((ai_url, ai_model, ai_key)):
            parsed = urlparse(ai_url)
            if (not all((ai_url, ai_model, ai_key)) or not parsed.hostname
                    or parsed.username or parsed.password or parsed.query or parsed.fragment
                    or parsed.port == 9000
                    or (parsed.scheme != "https" and ai_url != "http://dobolyi.com:9001/v1")):
                raise ValueError("Configure all three AI settings with an HTTPS base URL or the course port 9001 endpoint. Port 9000 is reserved for Hermes.")
        return cls(database, code, production, origin, build_id(), ai_url, ai_model, ai_key)
