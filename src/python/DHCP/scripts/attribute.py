from collections import defaultdict

TRUSTED_SERVERS_FILE = 'trusted_dhcp_servers.txt' # Название конфига с надёжными шлюзами
ALERT_THRESHOLD = 2 # Максимально допустимое количество запросов от одного подозрительного сервера
rogue_counter = defaultdict(int) # Счётчик подозрительных запросов от серверов
last_seen = {}  # Хранилище времени последнего запроса от каждого сервера

text2 = ""