
#include <iostream> // Для ввода/вывода в консоль
#include <string>   // Для работы со строками
#include <vector>   // Для работы с динамическими массивами
#include <sstream>  // Для работы с потоками строк (преобразование строк)
#include <fstream>  // Для работы с файлами (в данном коде не используется, но включен)
#include <map>      // Для работы с ассоциативными массивами (ключ-значение)
#include <algorithm> // Для использования алгоритмов, таких как transform, remove
#include <chrono>   // Для работы со временем (задержка)
#include <thread>   // Для работы с потоками (задержка)

// Директивы препроцессора для определения операционной системы
#ifdef _WIN32
#include <windows.h>   // Заголовочный файл для Windows API
#include <iphlpapi.h> // Заголовочный файл для IP Helper API (работа с сетью)
#pragma comment(lib, "IPHLPAPI.lib") // Указываем линковщику подключить библиотеку IPHLPAPI.lib (только для Windows)
#else
#include <unistd.h>    // Для функций POSIX (Linux, macOS)
#include <sys/socket.h> // Для работы с сокетами
#include <netinet/in.h> // Для структур адресов IPv4
#include <arpa/inet.h>  // Для преобразования IP-адресов
#include <ifaddrs.h>   // Для получения информации об интерфейсах
#include <net/if.h>    // Для работы с интерфейсами
#include <cstring>    // Для работы со строками в стиле C (например, strcpy)
#include <cstdlib>   // для стандартных функций C, таких как `malloc` и `free`
#endif

// Функция для выполнения команды в командной строке и получения вывода
std::string executeCommand(const std::string& command) {
    std::string result = ""; // Строка для хранения результата выполнения команды
#ifdef _WIN32 // Если компилируется под Windows
    FILE* pipe = _popen(command.c_str(), "r"); // Открываем канал для чтения вывода команды (используем _popen для Windows)
    if (pipe) { // Если канал успешно открыт
        char buffer[128]; // Буфер для чтения данных из канала
        while (!feof(pipe)) { // Пока не достигнут конец файла (канала)
            if (fgets(buffer, 128, pipe) != NULL) // Читаем строку из канала в буфер
                result += buffer; // Добавляем прочитанную строку к результату
        }
        _pclose(pipe); // Закрываем канал (используем _pclose для Windows)
    }
#else // Если компилируется не под Windows (Linux, macOS)
    FILE* pipe = popen(command.c_str(), "r"); // Открываем канал для чтения вывода команды (используем popen для POSIX)
    if (pipe) { // Если канал успешно открыт
        char buffer[128]; // Буфер для чтения данных из канала
        while (fgets(buffer, 128, pipe) != NULL) { // Пока не достигнут конец файла (канала)
            result += buffer; // Добавляем прочитанную строку к результату
        }
        pclose(pipe); // Закрываем канал (используем pclose для POSIX)
    }
#endif
    return result; // Возвращаем результат выполнения команды
}

// Функция для получения IP-адреса маршрутизирующего интерфейса (интерфейса, через который идет интернет)
std::string getRoutingInterface() {
#ifdef _WIN32 // Если компилируется под Windows
    DWORD dwSize = 0; // Размер необходимой структуры
    PIP_ADAPTER_INFO pAdapterInfo = NULL; // Указатель на структуру с информацией об адаптере
    if (GetAdaptersInfo(pAdapterInfo, &dwSize) == ERROR_BUFFER_OVERFLOW) { // Получаем размер необходимого буфера
        pAdapterInfo = (PIP_ADAPTER_INFO)malloc(dwSize); // Выделяем память под структуру
        if (!pAdapterInfo) return ""; // Allocation error // Если не удалось выделить память, возвращаем пустую строку
        if (GetAdaptersInfo(pAdapterInfo, &dwSize) == NO_ERROR) { // Получаем информацию об адаптерах
            for (PIP_ADAPTER_INFO pAdapter = pAdapterInfo; pAdapter != NULL; pAdapter = pAdapter->Next) { // Перебираем адаптеры
                if (pAdapter->GatewayList.IpAddress.String[0] != '\0') { // Если у адаптера есть шлюз
                    std::string result = pAdapter->IpAddressList.IpAddress.String; // Получаем IP-адрес адаптера
                    free(pAdapterInfo); // Освобождаем выделенную память
                    return result; // Возвращаем IP-адрес
                }
            }
        }
        free(pAdapterInfo); // Освобождаем выделенную память
    }
    return ""; // Если не удалось получить IP-адрес, возвращаем пустую строку
#else // Если компилируется не под Windows (Linux, macOS)
    struct ifaddrs* ifaddr, *ifa; // Структуры для хранения информации об интерфейсах
    std::string result = ""; // Строка для хранения результата
    if (getifaddrs(&ifaddr) == -1) { // Получаем информацию об интерфейсах
        return ""; // Если не удалось получить информацию, возвращаем пустую строку
    }

    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) { // Перебираем интерфейсы
        if (ifa->ifa_addr == NULL) { // Если адрес интерфейса не задан
            continue; // Переходим к следующему интерфейсу
        }
        if (ifa->ifa_addr->sa_family == AF_INET) { // Если адрес интерфейса - IPv4
            char host[NI_MAXHOST]; // Буфер для хранения имени хоста
            if(getnameinfo(ifa->ifa_addr, sizeof(struct sockaddr_in), host, NI_MAXHOST, NULL, 0, NI_NUMERICHOST) == 0){ // Получаем имя хоста
                
                if(std::string(ifa->ifa_name).find("lo") == std::string::npos){ // Проверяем, что интерфейс не loopback (lo)
                    result = std::string(host); // Записываем IP-адрес интерфейса в результат
                    break; // Прерываем цикл
                }
            }
        }
    }

    freeifaddrs(ifaddr); // Освобождаем выделенную память
    return result; // Возвращаем IP-адрес
#endif
}

// Функция для получения ARP-таблицы
std::vector<std::string> getArpTable() {
    std::string route = getRoutingInterface(); // Получаем IP-адрес маршрутизирующего интерфейса
    std::string command = ""; // Строка для хранения команды
#ifdef _WIN32 // Если компилируется под Windows
    command = "ARP -a -N " + route; // Формируем команду для получения ARP-таблицы
#else // Если компилируется не под Windows (Linux, macOS)
    command = "ip neigh"; // Using 'ip neigh' as 'arp -a' might require root on linux // Формируем команду для получения ARP-таблицы (используем 'ip neigh', так как 'arp -a' может требовать root)
#endif

    std::string output = executeCommand(command); // Выполняем команду и получаем вывод
    std::vector<std::string> lines; // Вектор для хранения строк вывода
    std::stringstream ss(output); // Создаем поток строк из вывода
    std::string line; // Строка для хранения текущей строки
    while (std::getline(ss, line)) { // Читаем строки из потока
        lines.push_back(line); // Добавляем строку в вектор
    }
    return lines; // Возвращаем вектор строк
}

// Функция для очистки и нормализации MAC-адреса
std::string cleanMacAddress(std::string mac_address) {
    std::transform(mac_address.begin(), mac_address.end(), mac_address.begin(), ::tolower); // Преобразуем строку в нижний регистр
    mac_address.erase(std::remove(mac_address.begin(), mac_address.end(), '-'), mac_address.end()); // Удаляем дефисы
    mac_address.erase(std::remove(mac_address.begin(), mac_address.end(), ':'), mac_address.end()); // Удаляем двоеточия

#ifdef _WIN32 // Если компилируется под Windows
   
    if(mac_address.length() == 12){ //Если длина MAC-адреса 12 символов (без разделителей)
          std::string final_mac_address; //Создаем результирующую строку
          for(size_t i=0; i < mac_address.length(); i++){ //Перебираем символы MAC-адреса
             final_mac_address += mac_address[i]; //Добавляем текущий символ в результирующую строку
             if((i+1)%2==0 && i != mac_address.length()-1){ //Если это второй символ пары и это не конец строки
                final_mac_address += ":"; //Добавляем разделитель (двоеточие)
             }
          }
            mac_address = final_mac_address; //Присваиваем MAC-адресу результирующую строку
    }
#else // Если компилируется не под Windows (Linux, macOS)
        if(mac_address.length() == 12){ //Если длина MAC-адреса 12 символов (без разделителей)
          std::string final_mac_address; //Создаем результирующую строку
          for(size_t i=0; i < mac_address.length(); i++){ //Перебираем символы MAC-адреса
             final_mac_address += mac_address[i]; //Добавляем текущий символ в результирующую строку
             if((i+1)%2==0 && i != mac_address.length()-1){ //Если это второй символ пары и это не конец строки
                final_mac_address += ":"; //Добавляем разделитель (двоеточие)
             }
          }
            mac_address = final_mac_address; //Присваиваем MAC-адресу результирующую строку
    }
#endif

     return mac_address; //Возвращаем очищенный MAC-адрес
}

// Функция для проверки наличия дублирующихся MAC-адресов
std::map<std::string, std::vector<std::string>> checkDuplicates(const std::vector<std::string>& arpTable) {
    std::map<std::string, std::vector<std::string>> macDict; // Создаем карту, где ключ - MAC-адрес, значение - вектор IP-адресов
    for (const auto& line : arpTable) { // Перебираем строки ARP-таблицы
        std::stringstream ss(line); // Создаем поток строк из текущей строки
        std::string part; // Строка для хранения части строки
        std::vector<std::string> parts; // Вектор для хранения частей строки
        while (ss >> part) { // Читаем части строки из потока
            parts.push_back(part); // Добавляем часть строки в вектор
        }
        if (parts.size() >= 3) { // Если в строке достаточно частей (IP-адрес, MAC-адрес и т.д.)
            std::string ipAddress = parts[0]; // Получаем IP-адрес
            std::string macAddress; // Строка для хранения MAC-адреса
#ifdef _WIN32 // Если компилируется под Windows
             if (parts.size() >= 2) { //Проверяем, есть ли MAC-адрес в строке
                macAddress = parts[1]; // Получаем MAC-адрес
            }
            else continue; //Если нет, переходим к следующей строке
#else // Если компилируется не под Windows (Linux, macOS)
            if(parts.size() >=6){ //Проверяем, есть ли MAC-адрес в строке (для Linux)
                macAddress = parts[4]; // Linux output uses the 5th element (MAC address) // Получаем MAC-адрес (для Linux)
            }
             else continue; //Если нет, переходим к следующей строке

#endif

           std::string macAddressCleaned = cleanMacAddress(macAddress); // Очищаем MAC-адрес
           if (macAddressCleaned == "ff:ff:ff:ff:ff:ff") continue; //Исключаем широковещательный MAC-адрес
           
            if (macDict.count(macAddressCleaned)) { // Если MAC-адрес уже есть в карте
                macDict[macAddressCleaned].push_back(ipAddress); // Добавляем IP-адрес в вектор
            }
            else { // Если MAC-адреса нет в карте
                macDict[macAddressCleaned] = { ipAddress }; // Создаем новую запись в карте с MAC-адресом и IP-адресом
            }
        }
    }

    std::map<std::string, std::vector<std::string>> duplicates; // Создаем карту для хранения дублирующихся MAC-адресов
    for (const auto& pair : macDict) { // Перебираем элементы карты MAC-адресов
        if (pair.second.size() > 1) { // Если у MAC-адреса больше одного IP-адреса (дубликат)
            duplicates[pair.first] = pair.second; // Добавляем MAC-адрес и его IP-адреса в карту дубликатов
        }
    }

    return duplicates; // Возвращаем карту дубликатов
}

// Функция для отключения интернет-соединения
void disableInternet() {
    try {
#ifdef _WIN32 // Если компилируется под Windows
        system("ipconfig /release"); // Выполняем команду для освобождения IP-адреса
#else // Если компилируется не под Windows (Linux, macOS)
       system("sudo ip link set dev wlan0 down"); // Replace wlan0 with your network interface name // Выполняем команду для отключения сетевого интерфейса (замените wlan0 на имя вашего интерфейса)
#endif
        std::cout << "Internet connection disabled." << std::endl; // Выводим сообщение об отключении интернета
    }
    catch (const std::exception& e) { // Ловим исключения
        std::cerr << "Error disabling internet: " << e.what() << std::endl; // Выводим сообщение об ошибке
    }
}

int main() {
    std::cout << "In case of detecting or attempting to detect an ARP attack on your device, it will be automatically disconnected from the wireless network. Do you agree to this?" << std::endl; // Выводим предупреждение
    std::string question; // Строка для хранения ответа пользователя
    std::cout << "Select Y/N: "; // Запрашиваем ответ
    std::cin >> question; // Читаем ответ
    if (question == "y" || question == "Y") { // Если ответ "y" или "Y"
        while (true) { // Бесконечный цикл
            std::vector<std::string> arpTable = getArpTable(); // Получаем ARP-таблицу
            std::map<std::string, std::vector<std::string>> duplicates = checkDuplicates(arpTable); // Проверяем наличие дубликатов MAC-адресов
            if (!duplicates.empty()) { // Если дубликаты найдены
                std::cout << "Duplicate MAC address found: " << std::endl; // Выводим сообщение
                for(const auto& pair : duplicates){ //Перебираем дубликаты
                    std::cout << "MAC: " << pair.first << ", IP: "; //Выводим MAC-адрес
                    for(const auto& ip : pair.second){ //Перебираем IP-адреса для текущего MAC-адреса
                        std::cout << ip << " "; //Выводим IP-адрес
                    }
                    std::cout << std::endl; //Переходим на новую строку
                }
                disableInternet(); // Отключаем интернет
            }
            else { // Если дубликаты не найдены
                std::cout << "No duplicates found." << std::endl; // Выводим сообщение
            }
             std::this_thread::sleep_for(std::chrono::seconds(5)); // Delay for 5 seconds // Задержка 5 секунд
        }
    }
    else { // Если ответ не "y" и не "Y"
        std::cout << "The program has been stopped" << std::endl; // Выводим сообщение об остановке программы
    }
    return 0; // Завершаем программу
}
