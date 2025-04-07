def check_duplicates(arp_table):

      alert_list = []

      arp_entries, mac = arp_table

      for i in range(len(arp_entries) - 1):
            if mac == arp_entries[i][1]:
                  alert_list.append(arp_entries[i])
      
      return(alert_list)