"""Exercise real Chromium startup, health refresh, reload and health failure recovery."""

import json
from pathlib import Path
import sys

from playwright.sync_api import expect, sync_playwright

from startup_support import running_server

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "results" / "browser"


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    errors = []
    with running_server(ROOT, Path(sys.executable), ARTIFACTS) as base, sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.on("requestfailed", lambda request: errors.append(f"Request failed: {request.url}"))
        page.on("response", lambda response: errors.append(f"HTTP {response.status}: {response.url}") if response.status >= 400 else None)
        try:
            page.goto(base, wait_until="networkidle")
            expect(page).to_have_title("Operations Tracking Application")
            expect(page.get_by_role("heading", name="Operations Tracking Application")).to_be_visible()
            expect(page.locator("#status")).to_have_text("Running")
            page.get_by_role("button", name="Refresh status").click()
            expect(page.locator("#status")).to_have_text("Running")
            page.reload(wait_until="networkidle")
            expect(page.locator("#status")).to_have_text("Running")
            # A valid HTTP response with invalid status checks the UI error path
            # without introducing an expected browser-console network failure.
            page.route("**/api/health", lambda route: route.fulfill(json={"status": "unavailable"}))
            page.get_by_role("button", name="Refresh status").click()
            expect(page.locator("#status")).to_have_text("Unavailable")
            expect(page.get_by_role("button", name="Refresh status")).to_be_enabled()
            page.unroute("**/api/health")
            page.get_by_role("button", name="Refresh status").click()
            expect(page.locator("#status")).to_have_text("Running")
            if errors:
                raise AssertionError("Browser errors: " + "; ".join(errors))
            page.screenshot(path=str(ARTIFACTS / "startup.png"), full_page=True)
            print("Chromium startup, refresh, reload and health recovery passed.")
        except BaseException:
            page.screenshot(path=str(ARTIFACTS / "failure.png"), full_page=True)
            raise
        finally:
            (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors, indent=2) + "\n", encoding="utf-8")
            context.tracing.stop(path=str(ARTIFACTS / "trace.zip"))
            browser.close()


if __name__ == "__main__":
    main()
