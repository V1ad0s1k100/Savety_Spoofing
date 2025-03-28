const historyElement = document.querySelector("[data-logs-history]");
const logsBar = document.querySelector("[data-logs-bar]");

let historyCount = 0;

historyElement.addEventListener("click", () => {
  logsBar.classList.toggle("logs-bar-block");
});

// =================================================

const stickCloseConfigElement = document.querySelector("[data-stick-close]");
const settingsBarElement = document.querySelector("[data-settings-bar]");
const btnOpenConfigElement = document.querySelector("[data-nav-btn]");

stickCloseConfigElement.addEventListener("click", () => {
  settingsBarElement.style.display = "none";
});

btnOpenConfigElement.addEventListener("click", () => {
  settingsBarElement.style.display = "flex";
});

// =================================

const dateElement = document.querySelector("[data-working-time]");

const mainBtnElement = document.querySelector("[data-main-btn]");
const loadingStatusElement = document.querySelector("[data-status-loading]");

let timeCount = 0;
let timer = null;

mainBtnElement.addEventListener("click", () => {
  if (timer === null) {
    dateElement.textContent = "00:00:01";
    let seconds = 1;

    timer = setInterval(() => {
      seconds++;
      const hours = String(Math.floor(seconds / 3600)).padStart(2, "0");
      const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(
        2,
        "0"
      );
      const secs = String(seconds % 60).padStart(2, "0");
      dateElement.textContent = `${hours}:${minutes}:${secs}`;
    }, 1000);

    loadingStatusElement.textContent = "There is an analysis";
  } else {
    clearInterval(timer);
    timer = null;
    dateElement.textContent = "00:00:00";
    loadingStatusElement.textContent = "Analysis stopped";
  }
});
