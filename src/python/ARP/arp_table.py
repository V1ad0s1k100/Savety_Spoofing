import scapy.all as scapy
import subprocess

def get_arp_table():
    route = scapy.conf.route.route("0.0.0.0")[1]
    command = ("ARP -a -N " + route)
    output = subprocess.check_output(command, shell=True)
    return output.decode('latin-1').splitlines()  # Изменено на 'latin-1' 