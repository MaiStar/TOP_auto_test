import os
import time
import urllib.request
import urllib.error

# Функция для форматирования времени в человеко-читаемый вид


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
        time_parts.append(
            f"{days} день{'/дня/дней' if days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14] else 'ь' if days == 1 else 'ей'}")
    if hours > 0:
        time_parts.append(
            f"{hours} час{'а/ов' if hours % 10 in [2, 3, 4] and hours % 100 not in [12, 13, 14] else '' if hours == 1 else 'ов'}")
    if minutes > 0:
        time_parts.append(
            f"{minutes} минут{'а/ы' if minutes % 10 in [2, 3, 4] and minutes % 100 not in [12, 13, 14] else 'а' if minutes == 1 else ''}")
    if seconds > 0 or not time_parts:
        time_parts.append(
            f"{seconds} секунд{'а/ы' if seconds % 10 in [2, 3, 4] and seconds % 100 not in [12, 13, 14] else 'а' if seconds == 1 else ''}")

    return ", ".join(time_parts)


# Чтение IP-адреса из файла auth
try:
    with open('auth', 'r') as file:
        lines = file.readlines()
        if len(lines) < 1:
            raise ValueError(
                "Файл auth должен содержать как минимум одну строку с IP-адресом")
        ip_address = lines[0].strip()
except FileNotFoundError:
    print("Файл auth не найден")
    exit(1)
except ValueError as e:
    print(e)
    exit(1)

# Путь к папке для сохранения скриншотов
screenshot_dir = 'jpg'

# Очистка папки jpg перед началом съемки
if os.path.exists(screenshot_dir):
    for file in os.listdir(screenshot_dir):
        os.remove(os.path.join(screenshot_dir, file))
else:
    os.makedirs(screenshot_dir)

# Запрос у пользователя количества скриншотов
try:
    num_screenshots = int(input("Сколько скриншотов вы хотите снять? "))
    if num_screenshots <= 0:
        raise ValueError
except ValueError:
    print("Пожалуйста, введите положительное целое число.")
    exit(1)

# Расчет общего времени выполнения в секундах
total_time_seconds = num_screenshots * 10

# Форматирование времени
formatted_time = format_time(total_time_seconds)

# Вывод времени выполнения
print(f"Съемка {num_screenshots} скриншотов займет {formatted_time}.")

# URL для снятия скриншота с использованием IP-адреса из файла
url = f"http://{ip_address}:85/image.jpg"

# Счетчики успешных и неуспешных попыток
success_count = 0
failure_count = 0

# Съемка скриншотов
for i in range(1, num_screenshots + 1):
    try:
        # Выполнение HTTP-запроса
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                # Сохранение скриншота
                screenshot_path = os.path.join(
                    screenshot_dir, f"screenshot_{i}.jpg")
                with open(screenshot_path, 'wb') as file:
                    file.write(response.read())
                success_count += 1
            else:
                failure_count += 1
    except urllib.error.URLError as e:
        print(f"Ошибка при снятии скриншота {i}: {e}")
        failure_count += 1
    # Пауза 10 секунд между снимками
    time.sleep(10)

# Подсчет процента успешных скриншотов
success_percentage = (success_count / num_screenshots) * \
    100 if num_screenshots > 0 else 0

# Вывод результата
print(
    f"Съемка завершена. Успешно снято {success_count} из {num_screenshots} скриншотов ({success_percentage:.2f}%).")
