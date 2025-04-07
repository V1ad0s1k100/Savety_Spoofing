const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("pythonAPI", {
  runScriptARP: (scriptPath) => ipcRenderer.invoke("python-run", scriptPath),
  runScriptDHCP: (scriptPath) => ipcRenderer.invoke("python-run", scriptPath),
});
