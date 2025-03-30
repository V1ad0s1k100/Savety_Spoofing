const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      devTools: true, // Включаем DevTools
      nodeIntegration: true, // Включает Node.js API в Renderer Process
      contextIsolation: false, // Отключает изоляцию контекста (для совместимости)
    },
  });

  mainWindow.loadFile("./public/index.html");
  mainWindow.setMenu(null);

  // Открываем DevTools
  mainWindow.webContents.openDevTools();
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
