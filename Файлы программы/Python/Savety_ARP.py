import pandas as pd
from pandas.api.types import CategoricalDtype
import pygame
import time
import subprocess 
import os 
import platform
import scapy.all as scapy
pygame.font.init()

def get_arp_table(): 
    route = scapy.conf.route.route("0.0.0.0")[1]
    command = ("ARP -a -N " + route)
    output = subprocess.check_output(command, shell=True) 
    return output.decode('latin-1').splitlines()  # Изменено на 'latin-1' 

def check_duplicates(arp_table):
    mac_dict = {}
    for line in arp_table:
        parts = line.split()
        if len(parts) >= 3:  # Убедимся, что строка содержит нужные данные 
            ip_address = parts[0]
            mac_address = parts[1] if platform.system() == "Windows" else parts[5]  # Для 'ip neigh' 
             
            # Приводим MAC-адрес к нижнему регистру и убираем разделители для сравнения 
            mac_address_cleaned = mac_address.lower().replace('-', ':') 

            # Исключаем MAC-адрес ff:ff:ff:ff:ff:ff 
            if mac_address_cleaned == 'ff:ff:ff:ff:ff:ff': 
                continue 
             
            if mac_address_cleaned in mac_dict: 
                mac_dict[mac_address_cleaned].append(ip_address)
            else:
                mac_dict[mac_address_cleaned] = [ip_address]
 
    return {mac: ips for mac, ips in mac_dict.items() if len(ips) > 1} 
 
def Savety_ARP(): 
    global text1
    global text2
    arp_table = get_arp_table() 
    duplicates = check_duplicates(arp_table) 
    if duplicates:
        text1 = "Найден дубликат MAC-адреса:" + str(duplicates)
        text2 = ''
        try:
            if platform.system() == "Windows":
                os.system("ipconfig /release")
            if platform.system() == "Linux":
                os.system("sudo ip link set dev wlan0 down") 
        except Exception as e:
            text1 = f"Ошибка при отключении интернета: {e}"
            text2 = ''
    else:
        text1 = "Дубликатов не найдено"
        text2 = ''

#Графика
W = 600
H = 400
WHITE = (255,255,255)
VOILET = (202, 160, 207)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
POSITION_BTN = ((W//2)-50,(H//2)-50)
POSITION_info = (0, H-50)

pygame.display.set_caption('Savety_ARP')
sc = pygame.display.set_mode((W, H))
sc.fill(VOILET)
pygame.display.set_icon(pygame.image.load('Изображения/PC.png'))
clock = pygame.time.Clock()
FPS = 30
count = 1
check_ARP = False

#Создание объектов
#В sc
pygame.draw.ellipse(sc, WHITE, (0, -100, W, 210))
#В btn
btn = pygame.Surface((100,100))
btn.fill(VOILET)
circle = pygame.draw.circle(btn, RED, (50,50), 25)
image_button = pygame.image.load('Изображения/Переключатель.png')
btn.blit(image_button, (0,0))

info = pygame.Surface((W,50))
info.fill(WHITE)
sc.blit(info, POSITION_info)
sc.blit(btn, POSITION_BTN)

#Тексты программы
#TITLE
text_title = pygame.font.SysFont('leelawadeeuisemilight', 60)
text_title_pos = text_title.render('BICU', 1, BLACK, WHITE)
sc.blit(text_title_pos, ((W//2)-60, 20))

#TEXT_INFO
text_info_1 = pygame.font.SysFont('calibri', 15)
text_info_2 = pygame.font.SysFont('calibri', 15)
text1 = 'В случае обнаружения или попытки обнаружения атаки MITM на ваше устройство,'
text2 = 'оно будет автоматически отключено от беспроводной сети'
text_info_pos_1 = text_info_1.render(text1, 1, BLACK, WHITE)
text_info_pos_2 = text_info_2.render(text2, 1, BLACK, WHITE)
sc.blit(text_info_pos_1, (10, H-40))
sc.blit(text_info_pos_2, (10, H-20))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #Отрисовка кнопок
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] < (W//2)+50 and event.pos[0] > (W//2)-50 and event.pos[1] < (H//2)+50 and event.pos[1] > (H//2)-50:
                #Красный
                if count%2==0:         
                    circle = pygame.draw.circle(btn, RED, (50,50), 25)
                    btn.blit(image_button, (0,0))
                    sc.blit(btn, POSITION_BTN)
                    sc.blit(info, POSITION_info)           
                    check_ARP = False
                #Зеленый
                if count%2!=0:
                    circle = pygame.draw.circle(btn, GREEN, (50,50), 25)
                    btn.blit(image_button, (0,0))
                    sc.blit(btn, POSITION_BTN)
                    sc.blit(info, POSITION_info)                    
                    check_ARP = True
                count +=1
        #Отрисовка текста в зависимости от цвета кнопки            
        if check_ARP:
            time.sleep(0.2)
            try:
                Savety_ARP()
            except (subprocess.CalledProcessError):
                continue
            text_info_pos_1 = text_info_1.render(text1, 1, BLACK, WHITE)
            text_info_pos_2 = text_info_2.render(text2, 1, BLACK, WHITE)
            sc.blit(text_info_pos_1, (10, H-40))
            sc.blit(text_info_pos_2, (10, H-20))
        if check_ARP ==False: 
            text_info_pos_1 = text_info_1.render('В случае обнаружения или попытки обнаружения атаки MITM на ваше устройство,', 1, (0,0,0), (255,255,255))
            text_info_pos_2 = text_info_2.render('оно будет автоматически отключено от беспроводной сети', 1, (0,0,0), (255,255,255))
            sc.blit(text_info_pos_1, (10, H-40))
            sc.blit(text_info_pos_2, (10, H-20))
    #Подгрузка всех изменений на этой итерации
    pygame.display.update()
    clock.tick(FPS)