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
        env["PYTHON_DOTENV_DISABLED"] = "1"
        env["AI_BASE_URL"] = "https://model.invalid/v1"
        env["AI_MODEL"] = "browser-synthetic-model"
        env["AI_API_KEY"] = "browser-test-only-key"
        with running_server(ROOT, Path(sys.executable), ARTIFACTS, launcher=True, env=env) as base, sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page = context.new_page()
            # UI response substitution only; provider parsing/limits use MockTransport in test_ai.py.
            # No real provider requests occur in this browser rehearsal.
            page.route("**/api/drafts/**", lambda route: route.fulfill(json={
                "text": "Synthetic draft: 8 modules recorded. <script>Never execute this text</script>",
                "day": "2026-11-10", "generated_at": "2026-11-10T20:00:00Z"}))
            page.on("pageerror", lambda error: errors.append(str(error)))
            try:
                page.goto(base, wait_until="networkidle")
                expect(page.get_by_role("heading", name="Open your team’s workday")).to_be_visible()
                page.get_by_label("Team access code", exact=True).fill(env["TEAM_ACCESS_CODE"])
                page.get_by_role("button", name="Open workspace", exact=True).click()
                expect(page.locator("#workspace")).to_be_visible()
                page.get_by_label("Workday Mountain time", exact=True).fill("2026-11-10")
                page.get_by_label("Workday Mountain time", exact=True).press("Tab")
                expect(page.locator("#save-job")).to_be_enabled()
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
                page.get_by_role("button", name="Draft customer update", exact=True).click()
                expect(page.locator("#customer-draft-text")).to_have_value("Synthetic draft: 8 modules recorded. <script>Never execute this text</script>")
                expect(page.get_by_role("button", name="Copy reviewed draft", exact=True)).to_be_disabled()
                page.get_by_label("I checked this draft against the saved records.", exact=True).check()
                expect(page.get_by_role("button", name="Copy reviewed draft", exact=True)).to_be_enabled()
                page.locator("#customer-draft-text").fill("Reviewed synthetic draft")
                expect(page.get_by_role("button", name="Copy reviewed draft", exact=True)).to_be_disabled()
                # A failed generation must remove the previous draft, with records still usable.
                page.route("**/api/drafts/customer/**", lambda route: route.fulfill(status=504, json={"detail":"The model took too long. No draft was saved or sent."}))
                page.get_by_role("button", name="Draft customer update", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("model took too long")
                expect(page.locator("#customer-output")).to_be_hidden()
                page.unroute("**/api/drafts/customer/**")
                page.get_by_label("Field notes optional", exact=True).fill("Unsaved test note")
                expect(page.get_by_role("button", name="Draft customer update", exact=True)).to_be_disabled()
                page.once("dialog", lambda dialog: dialog.accept())
                page.get_by_role("button", name="Discard changes", exact=True).click()
                page.reload(wait_until="networkidle")
                expect(page.locator("#job-count")).to_have_text("4")
                # An initial report failure must not advertise an export.
                page.route("**/api/report?*", lambda route: route.fulfill(status=503, json={"detail":"Report unavailable"}))
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#empty-report")).to_contain_text("Report unavailable")
                expect(page.locator("#export-link")).to_be_hidden()
                page.unroute("**/api/report?*")
                page.get_by_role("button", name="Refresh", exact=True).click()
                expect(page.locator("#report-rows")).to_contain_text("Browser verification job")
                expect(page.locator(".total").filter(has_text="Modules installed").locator("strong")).to_have_text("20")
                expect(page.locator(".total").filter(has_text="On-site hours").locator("strong")).to_have_text("6.0")
                page.get_by_role("button", name="Draft daily summary", exact=True).click()
                expect(page.locator("#report-draft-text")).to_have_value("Synthetic draft: 8 modules recorded. <script>Never execute this text</script>")
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
                # New-job drafts survive expiry/relogin and need an explicit retry.
                page.get_by_role("button", name="Add job", exact=True).click()
                page.get_by_label("Job name", exact=True).fill("Recovered new draft")
                page.get_by_label("Crew", exact=True).fill("Recovery crew")
                page.get_by_label("Site / location", exact=True).fill("Fictional recovery site")
                context.clear_cookies()
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#login-panel")).to_be_visible()
                page.get_by_label("Team access code", exact=True).fill(env["TEAM_ACCESS_CODE"])
                page.get_by_role("button", name="Open workspace", exact=True).click()
                expect(page.get_by_label("Job name", exact=True)).to_have_value("Recovered new draft")
                expect(page.locator("#save-state")).to_have_text("Unsaved changes")
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#job-count")).to_have_text("5")
                expect(page.locator("#save-state")).to_have_text("Saved")
                # Existing draft also survives; an intervening edit must still conflict.
                page.get_by_label("Field notes optional", exact=True).fill("Preserve my existing edit")
                context.clear_cookies()
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#login-panel")).to_be_visible()
                other = pw.request.new_context(base_url=base, extra_http_headers={"X-OTA-Request":"1"})
                other.post("/api/login", data={"code":env["TEAM_ACCESS_CODE"]})
                current = next(job for job in other.get("/api/jobs?day=2026-11-10").json()["jobs"] if job["title"] == "Recovered new draft")
                edited = {key:value for key,value in current.items() if key not in {"id","updated_at"}}
                edited["notes"] = "Another user saved this"
                assert other.put("/api/jobs/" + current["id"], data=edited).status == 200
                other.dispose()
                page.get_by_label("Team access code", exact=True).fill(env["TEAM_ACCESS_CODE"])
                page.get_by_role("button", name="Open workspace", exact=True).click()
                expect(page.get_by_label("Field notes optional", exact=True)).to_have_value("Preserve my existing edit")
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("changed or was removed")
                expect(page.get_by_label("Field notes optional", exact=True)).to_have_value("Preserve my existing edit")
                page.once("dialog", lambda dialog: dialog.accept())
                page.get_by_role("button", name="Refresh", exact=True).click()
                expect(page.get_by_label("Field notes optional", exact=True)).to_have_value("Another user saved this")
                # Previous-date results must disappear when the next report fails.
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#report-rows")).to_contain_text("Recovered new draft")
                page.get_by_role("button", name="Workday", exact=True).click()
                page.get_by_label("Workday Mountain time", exact=True).fill("2026-11-11")
                page.get_by_label("Workday Mountain time", exact=True).press("Tab")
                expect(page.locator("#job-count")).to_have_text("0")
                page.get_by_label("Job name", exact=True).fill("Next day only")
                page.get_by_label("Crew", exact=True).fill("Next day crew")
                page.get_by_label("Site / location", exact=True).fill("Example site B")
                page.get_by_role("button", name="Save job", exact=True).click()
                expect(page.locator("#save-state")).to_have_text("Saved")
                page.route("**/api/report?*", lambda route: route.fulfill(status=503, json={"detail":"Report unavailable"}))
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#empty-report")).to_contain_text("Report unavailable")
                expect(page.locator("#report-totals")).to_be_empty()
                expect(page.locator("#report-rows")).to_be_empty()
                expect(page.locator("#export-link")).to_be_hidden()
                page.unroute("**/api/report?*")
                page.get_by_role("button", name="Refresh", exact=True).click()
                expect(page.locator("#report-rows")).to_contain_text("Next day only")
                expect(page.locator("#report-rows")).not_to_contain_text("Recovered new draft")
                expect(page.locator("#export-link")).to_have_attribute("href", "/api/export?day=2026-11-11")
                page.route("**/api/report?*", lambda route: route.fulfill(status=503, json={"detail":"Report unavailable"}))
                page.get_by_role("button", name="Refresh", exact=True).click()
                expect(page.locator("#export-link")).to_be_hidden()
                expect(page.locator("#report-totals")).to_be_empty()
                page.unroute("**/api/report?*")
                page.get_by_role("button", name="Refresh", exact=True).click()
                expect(page.locator("#report-rows")).to_contain_text("Next day only")
                page.get_by_role("button", name="Workday", exact=True).click()
                page.set_viewport_size({"width":390,"height":844})
                page.screenshot(path=str(ARTIFACTS / "mobile-workday.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.get_by_role("button", name="Daily report", exact=True).click()
                expect(page.locator("#report-view")).to_be_visible()
                page.get_by_role("button", name="Draft daily summary", exact=True).click()
                expect(page.locator("#report-output")).to_be_visible()
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
