const historyElement = document.querySelector("[data-logs-history]");
const logsBar = document.querySelector("[data-logs-bar]");

let historyCount = 0;

historyElement.addEventListener("click", () => {
  logsBar.classList.toggle("logs-bar-block");
});

const stickCloseConfigElement = document.querySelector("[data-stick-close]");
const settingsBarElement = document.querySelector("[data-settings-bar]");
const btnOpenConfigElement = document.querySelector("[data-nav-btn]");

stickCloseConfigElement.addEventListener("click", () => {
  settingsBarElement.style.display = "none";
});

btnOpenConfigElement.addEventListener("click", () => {
  settingsBarElement.style.display = "flex";
});

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
});

dhcpSpoofingBtn.addEventListener("click", () => {
  mode = "DHCP";
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

    loadingStatusElement.textContent = "There is an analysis";

    // Запускаем цикл вызовов Python-скрипта при нажатии кнопки
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
        } else if (result[1] === "Error") {
          statusTitleElement.style.color = "red";
        } else {
          statusTitleElement.style.color = "#429442";
        }
      }, 1500);
    }
    if (mode === "DHCP") {
      console.log("DHCP mode was selected");
      // dhcpCheck = setInterval(async () => {
      //   let result = (
      //     await window.pythonAPI.runScript("src/python/DHCP/DHCP.py")
      //   )
      //     .replace("[", "")
      //     .replace("]", "")
      //     .replaceAll("'", "")
      //     .split(",");

      //   logsBar.textContent += result[0] + "\n";
      //   statusTitleElement.textContent = result[1];
      //   if (result[1] === "Warning") {
      //     statusTitleElement.style.color = "red";
      //   } else if (result[1] === "Error") {
      //     statusTitleElement.style.color = "red";
      //   } else {
      //     statusTitleElement.style.color = "#429442";
      //   }
      // }, 1500);
    }
  } else {
    clearInterval(arpCheck);
    clearInterval(dhcpCheck);
    clearInterval(timer);
    arpCheck = null;
    dhcpCheck = null;
    timer = null;
    setTimeout(() => {
      statusTitleElement.textContent = "";
    }, 1550);
    dateElement.textContent = "00:00:00";
    loadingStatusElement.textContent = "Analysis stopped";
  }
});
