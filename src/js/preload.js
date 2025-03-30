const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("pythonAPI", {
  runScript: (scriptPath) => ipcRenderer.invoke("python-run", scriptPath),
  onPythonData: (callback) => ipcRenderer.on("python-data", callback),
});
