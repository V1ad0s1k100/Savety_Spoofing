const { app, BrowserWindow, ipcMain } = require("electron");
const { exec } = require("child_process");
const path = require("path");

let isChecking = false;
let checkInterval;

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    autoHideMenuBar: true,
  });

  win.setIcon(path.join(__dirname, "image/icon/logo.png"));
  win.loadFile(path.join(__dirname, "index.html"));
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.on("start-check", (event) => {
  if (isChecking) {
    stopChecking(event);
  } else {
    startChecking(event);
  }
});

function stopChecking(event) {
  clearInterval(checkInterval);
  isChecking = false;
  event.sender.send("check-status", "Check stopped");
}

function startChecking(event) {
  isChecking = true;
  event.sender.send("check-status", "Check started");

  checkInterval = setInterval(() => {
    exec("arp -a", (error, stdout) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }

      const arpTable = parseArpTable(stdout);
      const duplicates = checkDuplicates(arpTable);

      if (duplicates.length > 0) {
        console.log("Duplicate MAC addresses found:", duplicates);
        event.sender.send(
          "check-status",
          `Duplicate MAC addresses found: ${JSON.stringify(duplicates)}`
        );
        handleDuplicates();
      } else {
        console.log("No duplicates found");
        event.sender.send("check-status", "No duplicates found");
      }
    });
  }, 2000);
}

function parseArpTable(stdout) {
  const lines = stdout.split("\n");
  const arpTable = [];
  let count = 0;

  lines.forEach((line) => {
    const parts = line.split(" ").filter((part) => part !== "");

    if (parts.length >= 3) {
      if (count != 0 && count != 1 && count != 2) {
        arpTable.push({
          ip: parts[0],
          mac: parts[1],
        });
      }
    }
    console.log(arpTable);
    count++;
  });

  return arpTable;
}

function checkDuplicates(arpTable) {
  let macDict = {};
  let duplicates = [];

  arpTable.forEach((entry) => {
    const macAddress = entry.mac.toLowerCase().replace(/-/g, ":");
    if (macAddress === "ff:ff:ff:ff:ff:ff") {
      return;
    }

    if (macDict[macAddress]) {
      macDict[macAddress].push(entry.ip);
      duplicates.push({ mac: macAddress, ips: macDict[macAddress] });
    } else {
      macDict[macAddress] = [entry.ip];
    }
  });

  return duplicates;
}

function handleDuplicates() {
  const platform = process.platform;
  const commands = {
    win32: "ipconfig /release",
    linux: "sudo ip link set dev wlan0 down && sudo ip link set dev wlan0 up",
  };

  const command = commands[platform];
  if (command) {
    exec(command, (error) => {
      if (error) {
        console.error(`Error handling duplicates: ${error}`);
      }
    });
  }
}
