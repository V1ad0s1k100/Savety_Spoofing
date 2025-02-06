const { ipcRenderer } = require("electron");

document.getElementById("checkButton").addEventListener("click", () => {
  ipcRenderer.send("start-check");
});

ipcRenderer.on("check-status", (event, message) => {
  document.querySelector(".notifications-container__title").textContent =
    message;
});
