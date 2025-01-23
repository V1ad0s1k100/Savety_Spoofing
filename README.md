Мы, студенты колледжа, обеспокоены вопросом безопасности данных в незащищённых локальных сетях для обычных пользователей (например, родственник автора зашёл в интернет-кафе, и через некоторое время на их аккаунтах была замечена подозрительная активность). Конечно, утилита нуждается в дальнейшем развитии, и мы продолжим над ней работать! Мы планируем создать .exe-файл для Windows и разработать его для Linux. Возможно, наша работа будет полезна некоторым разработчикам, и мы будем этому рады :)

## Подмена ARP-адреса

Подмена ARP-адреса — это атака на сетевом уровне, которая позволяет злоумышленнику изменить MAC-адрес отправителя в ARP-пакетах. Это может привести к перенаправлению трафика на ложный IP-адрес или другим нежелательным последствиям. Атака осуществляется путём отправки ложных ARP-ответов на запросы от других устройств в сети. Злоумышленник отправляет поддельные ARP-ответы, указывая свой MAC-адрес в качестве источника и IP-адрес жертвы в качестве получателя. Когда другие устройства в сети получают эти ложные ответы, они начинают отправлять трафик на ложный IP-адрес вместо фактического IP-адреса жертвы. Подмена ARP-адресов может использоваться в различных целях, например для кражи конфиденциальной информации, нарушения работы сетевых сервисов или просто для развлечения. Однако эту атаку можно обнаружить и предотвратить с помощью различных механизмов безопасности, таких как фильтрация ARP-пакетов, динамическая инфраструктура ARP или методы криптографической аутентификации.

### Способы защиты от подмены ARP:

- **Статические записи ARP**: вводятся вручную без автоматического изменения кэша ARP.
- **Программное обеспечение для проверки запросов ARP**: сертификация IP- и MAC-адресов и блокировка несанкционированных ответов.
- **Брандмауэры с фильтрацией пакетов**: обнаружение попыток хакеров выдать себя за другой хост.
- **Шифрование**: усложняет взлом ARP и защищает от чтения перехваченных сообщений.
- **VPN**: передача данных по зашифрованному туннелю, обеспечивающая защиту от хакерских атак.

Документация по библиотеке [Scapy](https://scapy.readthedocs.io/en/latest/index.html)

Если вы хотите поддержать нашу работу, вы можете сделать это здесь: Пожертвование: 5356 8624 4347 9193

We, college students, are concerned about data security in unsecured local networks for regular users (for example, the author's relative visited an internet cafe, and after some time, suspicious activity was noticed on their accounts). Of course, the utility needs further development, and we will continue to work on it! We plan to create an .exe file for Windows and develop it for Linux. Perhaps our work will be useful to some developers, and we will be glad :)

## ARP Spoofing

ARP spoofing is a network-level attack that allows an attacker to change the sender's MAC address in ARP packets. This can lead to traffic being redirected to a false IP address or other undesirable consequences. The attack is carried out by sending false ARP replies to requests from other devices on the network. The attacker sends fake ARP replies, indicating their MAC address as the source and the victim's IP address as the recipient. When other devices on the network receive these false replies, they start sending traffic to the false IP address instead of the victim's actual IP address. ARP spoofing can be used for various purposes, such as stealing confidential information, disrupting network services, or just for fun. However, this attack can be detected and prevented using various security mechanisms, such as ARP packet filtering, dynamic ARP infrastructure, or cryptographic authentication methods.

### Ways to protect against ARP spoofing:

- **Static ARP entries**: entered manually without automatic ARP cache changes.
- **Software for checking ARP requests**: certification of IP and MAC addresses and blocking unauthorized replies.
- **Firewalls with packet filtering**: detecting attempts by hackers to impersonate another host.
- **Encryption**: makes ARP spoofing more difficult and protects against reading intercepted messages.
- **VPN**: data transmission through an encrypted tunnel, providing protection against hacker attacks.

Documentation for the [Scapy](https://scapy.readthedocs.io/en/latest/index.html) library

If you want to support our work, you can do so here: Donation: 5356 8624 4347 9193
