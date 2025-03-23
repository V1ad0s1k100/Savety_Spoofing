import scapy.all as scapy # type: ignore
import time

def scan(ip):
    scapy.arping(ip) 
while True:
    print(scan('192.168.190.97/24'))