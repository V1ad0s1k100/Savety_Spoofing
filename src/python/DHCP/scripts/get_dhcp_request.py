import subprocess

def get_current_dhcp_request():
    #Определение текущего IP, полученного от DHCP
    output = subprocess.check_output("ipconfig", shell=True).decode('utf-8', errors='ignore')
    for line in output.splitlines():
        if "IPv4-адрес" in line or "IPv4 Address" in line:
            return line.split(":")[-1].strip()
    return None