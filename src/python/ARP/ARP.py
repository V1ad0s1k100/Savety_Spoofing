import os
from arp_table import *
from checkup_dub import *

def Savety_ARP():
    global text1
    global text2
    arp_table = get_arp_table()
    duplicates = check_duplicates(arp_table)
    if duplicates:
        text1 = "A duplicate of the MAC address was found: " + str(duplicates)
        text2 = "Warning"
        try:
            if platform.system() == "Windows":
                os.system("ipconfig /release")
        except Exception as e:
            text1 = f"Error when turning off the Internet: {e}"
            text2 = "Error"
    else:
        text1 = ""
        text2 = "Good"
    
    # Возвращаем значения для логирования
    return text1, text2

if __name__ == "__main__":
    result_text1, result_text2 = Savety_ARP()
    # Выводим результат для чтения в Node.js
    print([result_text1, result_text2])