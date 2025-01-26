# Перейти в директорию скрипта
cd $PSScriptRoot

# Компиляция
g++ code.cpp -o code -liphlpapi

# Запуск
if ($?) { .\code }