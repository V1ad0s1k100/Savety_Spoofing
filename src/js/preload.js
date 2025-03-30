const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("nodeAPI", {
  runPythonScript: () => {
    const { spawn } = require("child_process");
    const python = spawn("python", ["Savety_Spoofing/src/python/ARP/ARP.py"]);

    python.stdout.on("data", (data) => {
      console.log(`Output: ${data}`);
    });

    python.stderr.on("data", (data) => {
      console.error(`Error: ${data}`);
    });

    python.on("close", (code) => {
      console.log(`Process exited with code: ${code}`);
    });
  },
});
