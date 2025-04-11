const { app, BrowserWindow } = require("electron");
const { ipcMain } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, "./src/js/preload.js"),
    },
  });

  mainWindow.setMenu(null); // Отключение верхнего меню

  mainWindow.loadFile("./public/index.html");
};

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// Универсальная обработка запросов для запуска Python-скриптов
ipcMain.handle("python-run", (event, scriptPath) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn(scriptPath);

    let result = "";
    let error = "";

    // Получение данных из Python
    pythonProcess.stdout.on("data", (data) => {
      result += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      error += data.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0 || error) {
        reject(error || `Process exited with code ${code}`);
      } else {
        resolve(result);
      }
    });
  });
});
