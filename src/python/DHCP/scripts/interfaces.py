import subprocess
#Выключение интерфейсов
def disable_all_interfaces():
    subprocess.call(
        ["powershell", "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Disable-NetAdapter -Confirm:$false"],
        shell=True)
