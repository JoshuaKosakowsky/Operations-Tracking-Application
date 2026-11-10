"use strict";
const $ = (id) => document.getElementById(id);
const labels = {planned: "Planned", en_route: "On the way", on_site: "On site", complete: "Complete"};
const state = {jobs: [], selected: null, dirty: false, busy: false, view: "workday", day: "", session: null};
const numberFields = ["travel_minutes", "site_minutes", "miles", "modules"];

function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function notice(message, error = false) {
  $("notice").textContent = message;
  $("notice").classList.toggle("error", error);
  $("notice").hidden = !message;
}
async function api(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 45000);
  try {
    const response = await fetch(path, {...options, signal: controller.signal,
      headers: {"Content-Type": "application/json", "X-OTA-Request": "1", ...options.headers}});
    let body;
    try { body = await response.json(); } catch { throw new Error("The server could not respond. Wait a moment, then refresh."); }
    if (!response.ok) {
      if (response.status === 401 && path !== "/api/login") showLogin();
      throw new Error(body.detail || "The request failed. Try again.");
    }
    return body;
  } catch (error) {
    if (error.name === "AbortError") throw new Error("The request timed out. Refresh before retrying a save; it may already have reached the server.");
    if (error instanceof TypeError) throw new Error("Cannot reach the server. Check your connection; your unsaved fields remain here.");
    throw error;
  } finally { clearTimeout(timer); }
}
function canLeave() {
  if (state.busy) { notice("Please wait for the current request to finish."); return false; }
  return !state.dirty || window.confirm("Discard your unsaved changes?");
}
function markDirty(value) {
  state.dirty = value;
  $("save-state").textContent = value ? "Unsaved changes" : state.selected ? "Saved" : "Not saved yet";
}
function showLogin() {
  $("login-panel").hidden = false;
  $("workspace").hidden = true;
  $("logout").hidden = true;
  $("connection-text").textContent = "Sign in required";
}
function timeLabel(value) {
  const [hour, minute] = value.split(":").map(Number);
  return `${hour % 12 || 12}:${String(minute).padStart(2, "0")} ${hour >= 12 ? "pm" : "am"}`;
}
function fillForm(job) {
  state.selected = job || null;
  $("job-form").reset();
  if (job) for (const [name, value] of Object.entries(job)) {
    const input = $("job-form").elements.namedItem(name);
    if (input) input.value = value;
  }
  $("detail-title").textContent = job ? job.title : "Add a job";
  $("detail-eyebrow").textContent = job ? `${job.crew} · ${timeLabel(job.time)}` : "Ready for the next stop";
  $("delete-job").hidden = !job;
  $("customer-output").hidden = true;
  markDirty(false);
  renderJobs();
}
function renderJobs() {
  const filter = $("crew-filter").value;
  const crews = [...new Set(state.jobs.map(job => job.crew))].sort();
  $("crew-filter").replaceChildren(new Option("All crews", ""), ...crews.map(crew => new Option(crew, crew)));
  $("crew-filter").value = crews.includes(filter) ? filter : "";
  $("crew-options").replaceChildren(...crews.map(crew => new Option(crew, crew)));
  const visible = state.jobs.filter(job => !$("crew-filter").value || job.crew === $("crew-filter").value);
  $("job-count").textContent = state.jobs.length;
  $("job-list").replaceChildren(...visible.map(job => {
    const button = node("button", undefined, "job-card" + (state.selected?.id === job.id ? " selected" : ""));
    button.type = "button";
    button.setAttribute("aria-pressed", String(state.selected?.id === job.id));
    const top = node("span", undefined, "job-top");
    top.append(node("span", timeLabel(job.time)), node("span", labels[job.status], "status " + job.status));
    button.append(top, node("strong", job.title), node("span", job.crew, "job-meta"), node("span", job.site, "job-meta"));
    button.addEventListener("click", () => {
      if (!canLeave()) return;
      fillForm(job);
      if (window.matchMedia("(max-width: 700px)").matches) $("detail-title").scrollIntoView({block: "start"});
    });
    return button;
  }));
  $("empty-day").hidden = state.jobs.length > 0;
  $("empty-filter").hidden = !state.jobs.length || visible.length > 0;
}
async function loadDay(selectedId) {
  const data = await api(`/api/jobs?day=${encodeURIComponent(state.day)}`);
  state.jobs = data.jobs;
  fillForm(state.jobs.find(job => job.id === selectedId) || null);
  if (state.view === "report") await loadReport();
}
async function loadReport() {
  const report = await api(`/api/report?day=${encodeURIComponent(state.day)}`);
  const t = report.totals;
  const metrics = [[`${t.completed} / ${t.jobs}`, "Jobs complete", "saved jobs"],
    [(t.travel_minutes / 60).toFixed(1), "Travel hours", "crew time"],
    [(t.site_minutes / 60).toFixed(1), "On-site hours", "crew time"],
    [t.miles.toLocaleString(), "Miles recorded", "manual entries"],
    [t.modules.toLocaleString(), "Modules installed", t.modules_per_site_hour === null ? "No site time recorded" : `${t.modules_per_site_hour} per site hour`]];
  $("report-totals").replaceChildren(...metrics.map(([value, label, detail]) => {
    const item = node("div", undefined, "total");
    item.append(node("span", label), node("strong", value), node("span", detail));
    return item;
  }));
  $("report-rows").replaceChildren(...report.jobs.map(job => {
    const row = node("tr");
    for (const value of [job.title, job.crew, labels[job.status], `${job.travel_minutes} min`, `${job.site_minutes} min`, job.miles, job.modules]) row.append(node("td", value));
    return row;
  }));
  $("empty-report").hidden = report.jobs.length > 0;
  $("export-link").href = `/api/export?day=${encodeURIComponent(state.day)}`;
  $("report-output").hidden = true;
}
async function run(action) {
  if (state.busy) return;
  state.busy = true;
  $("save-job").disabled = true;
  for (const fieldset of $("job-form").querySelectorAll("fieldset")) fieldset.disabled = true;
  $("workspace").setAttribute("aria-busy", "true");
  try { await action(); } catch (error) { notice(error.message, true); }
  finally {
    state.busy = false; $("save-job").disabled = false;
    for (const fieldset of $("job-form").querySelectorAll("fieldset")) fieldset.disabled = false;
    $("workspace").removeAttribute("aria-busy");
  }
}
async function switchView(view) {
  if (!canLeave()) return;
  await run(async () => {
    markDirty(false);
    state.view = view;
    $("workday-view").hidden = view !== "workday";
    $("report-view").hidden = view !== "report";
    for (const name of ["workday", "report"]) {
      $(`${name}-tab`).classList.toggle("active", view === name);
      if (view === name) $(`${name}-tab`).setAttribute("aria-current", "page");
      else $(`${name}-tab`).removeAttribute("aria-current");
    }
    $("page-title").textContent = view === "workday" ? "The workday, in one place." : "Close the day with a clear picture.";
    $("page-description").textContent = view === "workday" ? "Plan the stops. Record the work. Keep the next person informed." : "Review the records, export the figures, and prepare the handover.";
    await loadDay(state.selected?.id);
  });
}
async function boot() {
  await run(async () => {
    state.session = await api("/api/session");
    $("build").textContent = `Build: ${state.session.build}`;
    $("build").title = state.session.build;
    if (!state.session.authenticated) { showLogin(); return; }
    $("login-panel").hidden = true;
    $("workspace").hidden = false;
    $("logout").hidden = !state.session.requires_code;
    $("connection-text").textContent = state.session.hosted ? "Team workspace" : "Local workspace";
    await loadDay(state.selected?.id);
  });
}

const parts = Object.fromEntries(new Intl.DateTimeFormat("en-US", {timeZone:"America/Denver",year:"numeric",month:"2-digit",day:"2-digit"}).formatToParts(new Date()).map(p => [p.type,p.value]));
state.day = `${parts.year}-${parts.month}-${parts.day}`;
$("workday-date").value = state.day;
$("workday-date").addEventListener("change", async () => {
  if (!$("workday-date").checkValidity() || !canLeave()) { $("workday-date").value = state.day; return; }
  const previous = state.day;
  state.day = $("workday-date").value;
  await run(async () => {
    try { await loadDay(); notice(""); }
    catch (error) { state.day = previous; $("workday-date").value = previous; throw error; }
  });
});
$("crew-filter").addEventListener("change", renderJobs);
$("workday-tab").addEventListener("click", () => switchView("workday"));
$("report-tab").addEventListener("click", () => switchView("report"));
$("new-job").addEventListener("click", () => { if (canLeave()) { fillForm(null); $("job-title").focus(); }});
$("discard").addEventListener("click", () => { if (canLeave()) fillForm(state.selected); });
$("refresh").addEventListener("click", () => { if (canLeave()) boot(); });
$("job-form").addEventListener("input", () => markDirty(true));
$("job-form").addEventListener("submit", event => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(event.target));
  for (const key of numberFields) values[key] = Number(values[key]);
  values.day = state.day;
  const existing = state.selected;
  if (existing) values.version = existing.version;
  run(async () => {
    const saved = await api(existing ? `/api/jobs/${existing.id}` : "/api/jobs", {method: existing ? "PUT" : "POST", body: JSON.stringify(values)});
    state.selected = saved;
    markDirty(false);
    await loadDay(saved.id);
    notice("Job saved. The daily report now includes these records.");
  });
});
$("delete-job").addEventListener("click", () => {
  if (state.busy || !state.selected || !window.confirm(`Delete “${state.selected.title}”? This removes its recorded work from the daily report.`)) return;
  run(async () => {
    await api(`/api/jobs/${state.selected.id}?version=${state.selected.version}`, {method:"DELETE"});
    markDirty(false); await loadDay(); notice("Job deleted.");
  });
});
$("example-day").addEventListener("click", () => {
  if (!canLeave()) return;
  run(async () => {
    const examples = [
      {title:"Example: roof survey",customer:"Example customer A",site:"North training site",crew:"Crew A",time:"08:00",status:"complete",travel_minutes:25,site_minutes:90,miles:12,modules:0,notes:"Fictional record. Survey finished; installation is not yet scheduled."},
      {title:"Example: panel installation",customer:"Example customer B",site:"West training site",crew:"Crew B",time:"09:30",status:"on_site",travel_minutes:35,site_minutes:150,miles:18,modules:12,notes:"Fictional record. First section installed; final inspection remains."},
      {title:"Example: system inspection",customer:"Example customer C",site:"South training site",crew:"Crew A",time:"14:00",status:"planned",travel_minutes:0,site_minutes:0,miles:0,modules:0,notes:"Fictional record. Confirm site access before leaving."},
    ];
    let added = 0;
    try {
      for (const example of examples) { await api("/api/jobs", {method:"POST",body:JSON.stringify({...example,day:state.day})}); added++; }
    } catch (error) {
      await loadDay();
      throw new Error(`${added} of 3 example jobs added. ${error.message}`);
    }
    await loadDay(); fillForm(state.jobs[0]); notice("Three fictional jobs added. Select a job, change its progress, and save it.");
  });
});
$("login-form").addEventListener("submit", async event => {
  event.preventDefault();
  await run(async () => {
    await api("/api/login", {method:"POST",body:JSON.stringify({code:$("access-code").value})});
    $("access-code").value = ""; notice("");
  });
  await boot();
});
$("logout").addEventListener("click", () => {
  if (!canLeave()) return;
  run(async () => { await api("/api/logout", {method:"POST"}); state.jobs=[]; fillForm(null); showLogin(); notice("Signed out."); });
});
window.addEventListener("beforeunload", event => { if (state.dirty) { event.preventDefault(); event.returnValue = ""; } });
boot();
