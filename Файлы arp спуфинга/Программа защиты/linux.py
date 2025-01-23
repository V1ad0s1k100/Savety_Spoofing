import subprocess
import os
import platform
import time
import scapy.all as scapy

def get_arp_table():
    command = "ip neigh"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8').splitlines()

def check_duplicates(arp_table):
    mac_dict = {}
    for line in arp_table:
        parts = line.split()
        if len(parts) >= 5:  # Убедимся, что строка содержит нужные данные
            ip_address = parts[0]
            mac_address = parts[4]  # MAC-адрес находится на 5-й позиции

            # Приводим MAC-адрес к нижнему регистру и убираем разделители для сравнения
            mac_address_cleaned = mac_address.lower()

            # Исключаем MAC-адрес ff:ff:ff:ff:ff:ff
            if mac_address_cleaned == 'ff:ff:ff:ff:ff:ff':
                continue

            if mac_address_cleaned in mac_dict:
                mac_dict[mac_address_cleaned].append(ip_address)
            else:
                mac_dict[mac_address_cleaned] = [ip_address]

    return {mac: ips for mac, ips in mac_dict.items() if len(ips) > 1}

def disable_internet(interface):
    try:
        os.system(f"sudo ip link set dev {interface} down")
    except Exception as e:
        print(f"Ошибка при отключении интернета: {e}")

print('В случае обнаружения или попытки обнаружения атаки ARP на ваше устройство, оно будет автоматически отключено от беспроводной сети. Вы согласны с этим?')
question = input('Выберите Y/N : ')
if question.lower() == "y":
    interface = input("Введите имя сетевого интерфейса (например, wlan0): ")

    while True:
        arp_table = get_arp_table()
        duplicates = check_duplicates(arp_table)
        if duplicates:
            print("Найден дубликат MAC-адреса:", duplicates)
            disable_internet(interface)
        else:
            print("Дубликатов не найдено.")

        time.sleep(5)  # Задержка в 5 секунд перед следующей проверкой
else:
    print('Программа была остановлена')