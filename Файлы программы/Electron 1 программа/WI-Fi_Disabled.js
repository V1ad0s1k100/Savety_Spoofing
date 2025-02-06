const { exec } = require("child_process");
function handleDuplicates() {
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

handleDuplicates()