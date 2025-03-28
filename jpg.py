import os
import time
import urllib.request
import urllib.error
import http.client

# Функция для форматирования времени


def format_time(seconds):
    if seconds == 0:
        return "0 секунд"
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} день" if days == 1 else f"{days} дня" if days in [
                          2, 3, 4] else f"{days} дней")
    if hours > 0:
        time_parts.append(f"{hours} час" if hours == 1 else f"{hours} часа" if hours in [
                          2, 3, 4] else f"{hours} часов")
    if minutes > 0:
        time_parts.append(f"{minutes} минута" if minutes == 1 else f"{minutes} минуты" if minutes in [
                          2, 3, 4] else f"{minutes} минут")
    if seconds > 0 or not time_parts:
        time_parts.append(f"{seconds} секунда" if seconds == 1 else f"{seconds} секунды" if seconds in [
                          2, 3, 4] else f"{seconds} секунд")
    return ", ".join(time_parts)

# Функция для получения uptime


def get_uptime(ip_address, username, password):
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(
        None, f"http://{ip_address}:85", username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    url = f"http://{ip_address}:85/cgi-bin/magicBox.cgi?action=getUptime"

    try:
        with opener.open(url, timeout=5) as response:
            content = response.read().decode('utf-8')
            if content.startswith("uptime="):
                return float(content.split("=")[1])
            return None
    except (urllib.error.URLError, ValueError, http.client.HTTPException):
        return None


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

# Путь к папке для скриншотов
screenshot_dir = 'jpg'
if os.path.exists(screenshot_dir):
    for file in os.listdir(screenshot_dir):
        os.remove(os.path.join(screenshot_dir, file))
else:
    os.makedirs(screenshot_dir)

# Ввод количества скриншотов
try:
    num_screenshots = int(input("Сколько скриншотов вы хотите снять? "))
    if num_screenshots <= 0:
        raise ValueError
except ValueError:
    print("Пожалуйста, введите положительное целое число.")
    exit(1)

# Пауза между скриншотами (в секундах)
pause_between_shots = 1

# Расчет общего времени
total_time_seconds = (num_screenshots - 1) * pause_between_shots

# Получение начального uptime
initial_uptime = get_uptime(ip_address, username, password)
if initial_uptime is None:
    print("Не удалось получить начальный uptime. Устройство может быть недоступно.")
    exit(1)

# Вывод начальной информации
print(
    f"Съемка {num_screenshots} скриншотов займет {format_time(total_time_seconds)}.")
days = int(initial_uptime // (24 * 3600))
remaining = initial_uptime % (24 * 3600)
hours = int(remaining // 3600)
remaining %= 3600
minutes = int(remaining // 60)
seconds = int(remaining % 60)
print(
    f"Начальное время работы: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд")

# URL для скриншотов
url = f"http://{ip_address}:85/image.jpg"

# Счетчики и флаги
success_count = 0
failure_count = 0
timeout = 5
start_time = time.time()
last_uptime = initial_uptime
reboot_detected = False
connection_issues = False  # Флаг для проблем с соединением

# Основной цикл съемки
for i in range(1, num_screenshots + 1):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            if response.status == 200:
                success_count += 1
            else:
                failure_count += 1
                connection_issues = True
                print(
                    f"Ошибка при снятии скриншота {i}: статус {response.status}")
    except urllib.error.URLError as e:
        failure_count += 1
        connection_issues = True
        if 'timed out' in str(e):
            print(f"Ошибка при снятии скриншота {i}: таймаут")
        else:
            print(f"Ошибка при снятии скриншота {i}: {e}")
    except http.client.HTTPException as e:
        failure_count += 1
        connection_issues = True
        print(f"Ошибка при снятии скриншота {i}: разрыв соединения ({e})")

    # Получение текущего uptime
    current_uptime = get_uptime(ip_address, username, password)

    # Проверка на перезагрузку
    if current_uptime is not None and last_uptime is not None:
        if current_uptime + 2 < last_uptime:  # Погрешность в 2 секунды
            reboot_detected = True
        last_uptime = current_uptime
    elif current_uptime is not None:
        last_uptime = current_uptime
    else:
        # Если uptime не удалось получить, считаем это проблемой соединения
        connection_issues = True

    # Расчет процентов и времени
    current_success_percentage = (success_count / i) * 100 if i > 0 else 0
    remaining_screenshots = num_screenshots - i
    elapsed_time = time.time() - start_time
    average_time_per_screenshot = elapsed_time / i if i > 0 else 0
    remaining_time_seconds = int(
        average_time_per_screenshot * remaining_screenshots)

    # Форматирование текущего uptime
    if current_uptime is not None:
        days = int(current_uptime // (24 * 3600))
        remaining = current_uptime % (24 * 3600)
        hours = int(remaining // 3600)
        remaining %= 3600
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        uptime_str = f"Время работы: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
    else:
        uptime_str = "Не удалось получить uptime (устройство недоступно)"

    # Вывод статуса
    print(f"{current_success_percentage:.0f}%. Снято {i} из {num_screenshots} скриншотов. "
          f"Осталось {remaining_screenshots} скриншотов, примерно {format_time(remaining_time_seconds)}.")
    print(f"Состояние: {'Была перезагрузка' if reboot_detected else 'Без перезагрузки'}"
          f"{' + проблемы с соединением' if connection_issues else ''}")
    print(uptime_str)

    if i < num_screenshots:
        time.sleep(pause_between_shots)

# Итоговый результат
success_percentage = (success_count / num_screenshots) * \
    100 if num_screenshots > 0 else 0
print(f"\nСъемка завершена.")
print(
    f"Успешно снято {success_count} из {num_screenshots} скриншотов ({success_percentage:.2f}%).")
print(f"Стабильность устройства: "
      f"{'Перезагрузка зафиксирована' if reboot_detected else 'Перезагрузок не было'}, "
      f"{'проблемы с соединением были' if connection_issues else 'соединение стабильно'}")
