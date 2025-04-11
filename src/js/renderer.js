// Блок с логами

const historyElement = document.querySelector("[data-logs-history]");
const logsBar = document.querySelector("[data-logs-bar]");

let historyCount = 0;

historyElement.addEventListener("click", () => {
  logsBar.classList.toggle("logs-bar-block");
});

// Блок с выбором защиты

const settingsBarElement = document.querySelector("[data-settings-bar]");
const btnOpenConfigElement = document.querySelector("[data-nav-btn]");
const btnOpenConfigTitleElement = document.querySelector(
  "[data-nav-btn-title]"
);
const triangleBtnConfigElement = document.querySelector(
  "[data-nav-btn-triangle]"
);

let btnOpenConfigCount = 0;

btnOpenConfigElement.addEventListener("click", () => {
  if (btnOpenConfigCount % 2 === 0) {
    settingsBarElement.style.display = "flex";
    settingsBarElement.style.animation = "appearance_from_below 0.2s ease-out";
    triangleBtnConfigElement.style.rotate = "360deg";
  } else {
    settingsBarElement.style.display = "none";
    triangleBtnConfigElement.style.rotate = "270deg";
  }
  btnOpenConfigCount++;
});

// Блок главной кнопки, таймера и статуса

const dateElement = document.querySelector("[data-working-time]");
const mainBtnElement = document.querySelector("[data-main-btn]");
const loadingStatusElement = document.querySelector("[data-status-loading]");
const statusTitleElement = document.querySelector("[data-status]");

let timer = null;
let arpCheck = null;
let dhcpCheck = null;
let mode = "";

const arpSpoofingBtn = document.querySelector("[data-arp-spoofing-btn]");
const dhcpSpoofingBtn = document.querySelector("[data-dhcp-spoofing-btn]");
const mainBtn = document.querySelector("[data-main-btn]");

arpSpoofingBtn.addEventListener("click", () => {
  mode = "ARP";
  btnOpenConfigTitleElement.textContent = mode;
  settingsBarElement.style.display = "none";
  btnOpenConfigCount++;
  triangleBtnConfigElement.style.rotate = "270deg";
});

dhcpSpoofingBtn.addEventListener("click", () => {
  mode = "DHCP";
  btnOpenConfigTitleElement.textContent = mode;
  settingsBarElement.style.display = "none";
  btnOpenConfigCount++;
  triangleBtnConfigElement.style.rotate = "270deg";
});

mainBtnElement.addEventListener("click", () => {
  if (!timer && mode !== "") {
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

    // Добавить вывод ...

    loadingStatusElement.textContent = "Анализ...";

    if (mode === "ARP") {
      arpCheck = setInterval(async () => {
        let result = (await window.pythonAPI.runScript("src/python/ARP/ARP.py"))
          .replace("[", "")
          .replace("]", "")
          .replaceAll("'", "")
          .split(",");

        logsBar.textContent += result[0] + "\n";
        statusTitleElement.textContent = result[1];
        if (result[1] === "Warning") {
          statusTitleElement.style.color = "red";
        } else {
          statusTitleElement.style.color = "#429442";
        }
      }, 1500);
    }
    if (mode === "DHCP") {
      dhcpCheck = setInterval(async () => {
        let result = await window.pythonAPI.runScript(
          "src/python/DHCP/DHCP.py"
        );
      }, 1500);
    }
  } else {
    if (mode === "ARP") {
      clearTimeout(arpCheck);
      arpCheck = null;
    } else if (mode === "DHCP") {
      clearTimeout(dhcpCheck);
      dhcpCheck = null;
    }

    clearInterval(timer);
    timer = null;
    statusTitleElement.textContent = "";
    dateElement.textContent = "00:00:00";
    if (mode !== "") {
      loadingStatusElement.textContent = "Анализ остановлен";
    } else {
      loadingStatusElement.textContent = "Выбирете тип защиты";
    }
  }
});
