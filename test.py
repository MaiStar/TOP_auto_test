import urllib.request
import urllib.error

# Чтение данных из файла auth
try:
    with open('auth', 'r') as file:
        lines = file.readlines()
        if len(lines) != 3:
            raise ValueError(
                "Файл auth должен содержать ровно три строки: IP-адрес, логин, пароль")
        ip_address = lines[0].strip()
        username = lines[1].strip()
        password = lines[2].strip()
except FileNotFoundError:
    print("Файл auth не найден")
    exit(1)
except ValueError as e:
    print(e)
    exit(1)

# Настройка аутентификации для HTTP-запроса
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, f"http://{ip_address}:85", username, password)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)

# Формирование URL для запроса
url = f"http://{ip_address}:85/cgi-bin/magicBox.cgi?action=getUptime"

# Выполнение запроса и обработка ошибок
try:
    with opener.open(url) as response:
        content = response.read().decode('utf-8')
except urllib.error.URLError as e:
    print(f"Ошибка при выполнении запроса: {e}")
    exit(1)

# Обработка ответа в формате uptime=44201.67
if content.startswith("uptime="):
    uptime_str = content.split("=")[1]
    try:
        uptime_seconds = float(uptime_str)  # Преобразование строки в число
    except ValueError:
        print("Некорректный формат ответа")
        exit(1)
else:
    print("Некорректный формат ответа")
    exit(1)

# Перевод секунд в дни, часы, минуты и секунды
days = int(uptime_seconds // (24 * 3600))  # Целые дни
uptime_seconds %= (24 * 3600)              # Остаток после дней
hours = int(uptime_seconds // 3600)        # Целые часы
uptime_seconds %= 3600                     # Остаток после часов
minutes = int(uptime_seconds // 60)        # Целые минуты
seconds = int(uptime_seconds % 60)         # Оставшиеся секунды

# Вывод результата
print(
    f"Время работы: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд")
