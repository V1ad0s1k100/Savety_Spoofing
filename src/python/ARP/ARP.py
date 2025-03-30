from arp_table import *
from checkup_dub import *

def Savety_ARP():
    global text1
    global text2
    arp_table = get_arp_table() 
    duplicates = check_duplicates(arp_table) 
    if duplicates:
        text1 = "Найден дубликат MAC-адреса:" + str(duplicates)
        text2 = 'Warning'
        try:
            if platform.system() == "Windows":
                os.system("ipconfig /release")
            if platform.system() == "Linux":
                os.system("sudo ip link set dev wlan0 down") 
        except Exception as e:
            text1 = f"Ошибка при отключении интернета: {e}"
            text2 = ''
    else:
        text1 = "Good"
        text2 = ''
    
    # Возвращаем значения для логирования
    return text1, text2

if __name__ == "__main__":
    result_text1, result_text2 = Savety_ARP()
    print(result_text1)  # Выводим результат для чтения в Node.js
    if result_text2:
        print(result_text2)  # Выводим предупреждение, если есть