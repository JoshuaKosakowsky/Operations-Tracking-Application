"use strict";

const statusOutput = document.querySelector("#status");
const refreshButton = document.querySelector("#refresh");

async function refreshStatus() {
  refreshButton.disabled = true;
  statusOutput.textContent = "Checking";
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    if (!response.ok) throw new Error("Health request failed");
    const health = await response.json();
    if (health.status !== "ok") throw new Error("Unexpected health response");
    statusOutput.textContent = "Running";
  } catch {
    statusOutput.textContent = "Unavailable";
  } finally {
    refreshButton.disabled = false;
  }
}

refreshButton.addEventListener("click", refreshStatus);
refreshStatus();
