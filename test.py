import urllib.request
import urllib.error
import urllib.parse

# 1. Запрашиваем IP-адрес у пользователя
ip_address = input("Введите IP-адрес в формате 192.168.0.78: ")

# 2. Настраиваем аутентификацию для HTTP-запроса
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, f"http://{ip_address}:85", "admin", "123456")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)

# Формируем URL для запроса
url = f"http://{ip_address}:85/cgi-bin/magicBox.cgi?action=getUptime"

# Выполняем запрос и обрабатываем возможные ошибки
try:
    with opener.open(url) as response:
        content = response.read().decode('utf-8')
except urllib.error.URLError as e:
    print(f"Ошибка при выполнении запроса: {e}")
    exit(1)

# 3. Обрабатываем ответ в формате uptime=44201.67
if content.startswith("uptime="):
    uptime_str = content.split("=")[1]
    try:
        uptime_seconds = float(uptime_str)  # Преобразуем строку в число
    except ValueError:
        print("Некорректный формат ответа")
        exit(1)
else:
    print("Некорректный формат ответа")
    exit(1)

# Переводим секунды в дни, часы, минуты и секунды
days = int(uptime_seconds // (24 * 3600))  # Целые дни
uptime_seconds %= (24 * 3600)              # Остаток после дней
hours = int(uptime_seconds // 3600)        # Целые часы
uptime_seconds %= 3600                     # Остаток после часов
minutes = int(uptime_seconds // 60)        # Целые минуты
seconds = int(uptime_seconds % 60)         # Оставшиеся секунды

# Выводим результат в читаемом формате
print(
    f"Время работы: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд")
