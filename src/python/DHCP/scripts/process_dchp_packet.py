import time
from scapy.layers.dhcp import DHCP
from scripts.interfaces import disable_all_interfaces

def process_dhcp_packet(packet, trusted_servers, last_seen, rogue_counter, ALERT_THRESHOLD):
    # Обработка пакетов на выявление нехорошего
    if DHCP in packet and packet[DHCP].options:
        for opt in packet[DHCP].options:
            if opt[0] == 'server_id':
                dhcp_server = opt[1]

                # Проверка, если сервер уже был обработан недавно (например, 1 секунда назад)
                current_time = time.time()
                if dhcp_server not in trusted_servers and (
                        dhcp_server not in last_seen or current_time - last_seen[dhcp_server] > 1):
                    rogue_counter[dhcp_server] += 1
                    text2 = "Warning"
                    last_seen[dhcp_server] = current_time  # Обновляем время последнего запроса
                    if rogue_counter[dhcp_server] >= ALERT_THRESHOLD:
                        disable_all_interfaces()
                    break