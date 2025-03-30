import platform

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