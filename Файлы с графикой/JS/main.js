const { app, BrowserWindow, ipcMain } = require("electron"); // Импортируем необходимые модули из Electron
const { exec } = require("child_process"); // Импортируем модуль для выполнения команд в командной строке

let isChecking = false; // Флаг для отслеживания состояния проверки
let checkInterval; // Переменная для хранения интервала проверки

function createWindow() {
  // Функция для создания окна приложения
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    autoHideMenuBar: true,
  });

  win.loadFile("index.html"); // Загружаем HTML файл в окно
}

app.whenReady().then(createWindow); // Создаем окно, когда приложение готово

app.on("window-all-closed", () => {
  // Закрываем приложение, если все окна закрыты (кроме macOS)
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // Создаем новое окно, если приложение активировано и нет открытых окон (для macOS)
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.on("start-check", (event) => {
  // Обработчик события для начала/остановки проверки
  if (isChecking) {
    clearInterval(checkInterval); // Останавливаем интервал проверки
    isChecking = false;
    event.sender.send("check-status", "Check stopped"); // Отправляем статус в рендерер
    console.log("Check stopped");
  } else {
    isChecking = true;
    event.sender.send("check-status", "Check started"); // Отправляем статус в рендерер
    console.log("Check started");

    function checkDuplicates(arpTable) {
      // Функция для проверки дубликатов MAC-адресов
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
      // Функция для обработки дубликатов MAC-адресов
      const platform = process.platform;
      try {
        if (platform === "win32") {
          exec("ipconfig /release", (error) => {
            if (error) {
              console.error(`Error releasing IP: ${error}`);
            }
          });
        } else if (platform === "linux") {
          exec("sudo ip link set dev wlan0 down", (error) => {
            if (error) {
              console.error(`Error disabling network interface: ${error}`);
            }
          });
        }
      } catch (e) {
        console.error(`Error handling duplicates: ${e}`);
      }
    }

    checkInterval = setInterval(() => {
      // Устанавливаем интервал для выполнения проверки каждые 2 секунды
      exec("arp -a", (error, stdout) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }

        const lines = stdout.split("\n");
        const arpTable = [];

        lines.forEach((line) => {
          const parts = line.split(" ").filter((part) => part !== "");
          if (parts.length >= 3) {
            arpTable.push({
              ip: parts[0],
              mac: parts[1],
            });
          }
        });

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
});
