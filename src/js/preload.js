const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("pythonAPI", {
  runScript: (scriptPath) => ipcRenderer.invoke("python-run", scriptPath),
});
