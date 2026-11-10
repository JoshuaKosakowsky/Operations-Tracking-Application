"""Exercise a complete workday through the normal launcher in desktop and mobile Chromium."""

import json
import os
from pathlib import Path
import sys
import tempfile

from playwright.sync_api import expect, sync_playwright

from startup_support import running_server

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "results" / "browser"


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    errors = []
    with tempfile.TemporaryDirectory(prefix="ota-browser-") as temporary:
        env = os.environ.copy()
        for key in list(env):
            if key.startswith(("OPENAI_", "GOOGLE_", "APP_", "TEAM_", "AI_")) or key == "DATABASE_URL":
                env.pop(key, None)
        env["DATABASE_URL"] = "sqlite:///" + (Path(temporary) / "browser.db").as_posix()
        env["APP_ENV"] = "local"
        env["TEAM_ACCESS_CODE"] = "browser-test-only-shared-code"
        env["OPENAI_API_KEY"] = ""
        with running_server(ROOT, Path(sys.executable), ARTIFACTS, launcher=True, env=env) as base, sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            try:
                page.goto(base, wait_until="networkidle")
                expect(page.get_by_role("heading", name="Open your team’s workday")).to_be_visible()
                page.get_by_label("Team access code", exact=True).fill(env["TEAM_ACCESS_CODE"])
                page.get_by_role("button", name="Open workspace", exact=True).click()
                expect(page.locator("#workspace")).to_be_visible()
                page.get_by_role("button", name="Try example workday").click()
                expect(page.locator("#job-count")).to_have_text("3")
                page.get_by_role("button", name="Add job", exact=True).click()
                page.get_by_label("Job name", exact=True).fill("Browser verification job")
                page.get_by_label("Crew", exact=True).fill("Test crew")
                page.get_by_label("Site / location", exact=True).fill("Fictional test site")
                page.get_by_label("Progress", exact=True).select_option("complete")
                page.get_by_label("On site minutes", exact=True).fill("120")
                page.get_by_label("Modules installed", exact=True).fill("8")
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#save-state")).to_have_text("Saved")
                expect(page.locator("#job-count")).to_have_text("4")
                page.reload(wait_until="networkidle")
                expect(page.locator("#job-count")).to_have_text("4")
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#report-rows")).to_contain_text("Browser verification job")
                expect(page.locator("#report-totals")).to_contain_text("20")
                with page.expect_download() as download:
                    page.get_by_role("link", name="Download CSV").click()
                assert "Browser verification job" in Path(download.value.path()).read_text()
                page.screenshot(path=str(ARTIFACTS / "desktop-report.png"), full_page=True)
                page.get_by_role("button", name="Workday", exact=True).click()
                page.locator(".job-card").filter(has_text="Browser verification job").click()
                page.get_by_label("Field notes optional", exact=True).fill("Keep this unsaved note on failure")
                # Bounded synthetic storage failure; the UI must retain user input.
                page.route("**/api/jobs/*", lambda route: route.fulfill(status=503, json={"detail":"Storage temporarily unavailable"}))
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("Storage temporarily unavailable")
                expect(page.get_by_label("Field notes optional", exact=True)).to_have_value("Keep this unsaved note on failure")
                page.unroute("**/api/jobs/*")
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#save-state")).to_have_text("Saved")
                page.set_viewport_size({"width":390,"height":844})
                page.screenshot(path=str(ARTIFACTS / "mobile-workday.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#report-view")).to_be_visible()
                page.screenshot(path=str(ARTIFACTS / "mobile-report.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.get_by_role("button", name="Sign out", exact=True).click()
                expect(page.get_by_role("heading", name="Open your team’s workday")).to_be_visible()
                if errors:
                    raise AssertionError("Browser errors: " + "; ".join(errors))
                print("Normal-launch desktop/mobile login, create, update, persistence, report, export, failure recovery and logout passed.")
            except BaseException:
                page.screenshot(path=str(ARTIFACTS / "failure.png"), full_page=True)
                raise
            finally:
                (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors) + "\n")
                context.tracing.stop(path=str(ARTIFACTS / "trace.zip"))
                browser.close()


if __name__ == "__main__":
    main()
