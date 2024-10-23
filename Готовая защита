import subprocess 
import os 
import platform 
import time
import scapy.all as scapy

def get_arp_table(): 
    route = scapy.conf.route.route("0.0.0.0")[1]
    command = ("ARP -a -N " + route)
    output = subprocess.check_output(command, shell=True) 
    return output.decode('latin-1').splitlines()  # Изменено на 'latin-1' 

def check_duplicates(arp_table): 
    mac_dict = {} 
    for line in arp_table: 
        parts = line.split() 
        if len(parts) >= 3:  # Убедимся, что строка содержит нужные данные 
            ip_address = parts[0] 
            mac_address = parts[1] if platform.system() == "Windows" else parts[5]  # Для 'ip neigh' 
             
            # Приводим MAC-адрес к нижнему регистру и убираем разделители для сравнения 
            mac_address_cleaned = mac_address.lower().replace('-', ':') 

            # Исключаем MAC-адрес ff:ff:ff:ff:ff:ff 
            if mac_address_cleaned == 'ff:ff:ff:ff:ff:ff': 
                continue 
             
            if mac_address_cleaned in mac_dict: 
                mac_dict[mac_address_cleaned].append(ip_address) 
            else: 
                mac_dict[mac_address_cleaned] = [ip_address] 
 
    return {mac: ips for mac, ips in mac_dict.items() if len(ips) > 1} 
 
def disable_internet(): 
    try: 
        if platform.system() == "Windows": 
            os.system("ipconfig /release") 
        else: 
            os.system("sudo ip link set dev wlan0 down")  # Замените <интерфейс> на нужный 
    except Exception as e: 
        print(f"Ошибка при отключении интернета: {e}") 
print('В случае обнаружения или попытки обнаружения атаки ARP на ваше устройство, оно будет автоматически отключено от беспроводной сети. Вы согласны с этим?')
question = input('Выберите Y/N : ')
if question == "y" or question == "Y":

    while True: 
        arp_table = get_arp_table() 
        duplicates = check_duplicates(arp_table) 
        if duplicates: 
            print("Найден дубликат MAC-адреса:", duplicates) 
            disable_internet() 
        else: 
            print("Дубликатов не найдено.") 
        
        time.sleep(5)  # Задержка в 10 секунд перед следующей проверкой
else:
    print('Программа была остановлена')
