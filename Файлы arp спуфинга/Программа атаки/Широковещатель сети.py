import scapy.all as scapy # type: ignore
import time

def scan(ip):   #scapy.arping(ip) <--- упрощенная версия написанного снизу

    arp_request = scapy.ARP(pdst = ip) #Создание ARP пакета с указанием широковещательного ip-адреса

    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff') #Создание фрэйма для отправки ARP пакета. dst = 'ff:ff:ff:ff:ff:ff' <--- широковещательный mac-адрес в сети, src = 'f8:5e:a0:22:fe:b5' <--- mac-адрес моего ПК

    arp_request_broadcast = broadcast/arp_request #Объединяем фрейм и ARP

    #Отправка пакета

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]
    print('\tIP\t\t\t\t\tMAC Adress\n--------------------------------------')
    for element in answered_list:
        print(str(element[1].psrc)+"\t\t"+str(element[1].hwsrc))
while True:
    print(scan('192.168.31.1/24'))
    time.sleep(1)