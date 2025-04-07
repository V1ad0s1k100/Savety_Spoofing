import scapy.all as scapy
import subprocess
import re

def get_arp_table():
      route = scapy.conf.route.route("0.0.0.0")[1]
      command = f"arp -a -N {route}"
      result = subprocess.check_output(command, shell=True, text=True)
      
      arp_entries_ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", result)

      arp_entries_mac = re.findall(r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})", result)

      arp_entries = []

      for i in range(1, len(arp_entries_ip)):
            if i < len(arp_entries_mac):
                  arp_entries.append([arp_entries_ip[i], arp_entries_mac[i]])
            else:
                  arp_entries.append([arp_entries_ip[i], " "])
      if len(arp_entries_mac) > 0:
            return [arp_entries, arp_entries_mac[0]]
      else:
            return [arp_entries, "1"]
