from scapy.all import *
from scripts.attribute import TRUSTED_SERVERS_FILE, last_seen, rogue_counter, ALERT_THRESHOLD
from scripts.process_dchp_packet import process_dhcp_packet

# Запуск (если файла с конфигом нету, он создастся)
if not os.path.exists(TRUSTED_SERVERS_FILE):
    with open(TRUSTED_SERVERS_FILE, "w") as file:
        file.write("# Доверенные DHCP-серверы. По умолчанию указаны стандартные шлюзы, через снос строки можно указать свои шлюзы\n")
        file.write("192.168.0.1\n")
        file.write("192.168.1.1\n")

with open(TRUSTED_SERVERS_FILE, "r") as file:
    trusted_servers = [line.strip() for line in file if not line.startswith("#") and line.strip()]

sniff(filter="udp and (port 67 or port 68)",
      prn=lambda packet: process_dhcp_packet(packet, trusted_servers, last_seen, rogue_counter, ALERT_THRESHOLD),
      store=0)
