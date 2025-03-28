import os
import time
import urllib.request
import urllib.error

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


# Чтение IP-адреса из файла auth
try:
    with open('auth', 'r') as file:
        ip_address = file.readline().strip()
except FileNotFoundError:
    print("Файл auth не найден")
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

# Пауза между скриншотами как переменная (в секундах)
pause_between_shots = 1  # Можно изменить, например, на 1, 5, 15 и т.д.

# Расчет общего времени (паузы между скриншотами)
total_time_seconds = (num_screenshots - 1) * pause_between_shots
print(
    f"Съемка {num_screenshots} скриншотов займет {format_time(total_time_seconds)}.")

# URL для скриншотов
url = f"http://{ip_address}:85/image.jpg"

# Счетчики
success_count = 0
failure_count = 0

# Начало съемки
start_time = time.time()

# Основной цикл съемки
for i in range(1, num_screenshots + 1):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                success_count += 1
                # Раскомментируйте, если нужно сохранять файлы
                # screenshot_path = os.path.join(screenshot_dir, f"screenshot_{i}.jpg")
                # with open(screenshot_path, 'wb') as file:
                #     file.write(response.read())
            else:
                failure_count += 1
    except urllib.error.URLError as e:
        print(f"Ошибка при снятии скриншота {i}: {e}")
        failure_count += 1

    # Текущий процент успеха
    current_success_percentage = (success_count / i) * 100 if i > 0 else 0

    # Оставшиеся скриншоты
    remaining_screenshots = num_screenshots - i

    # Расчет оставшегося времени на основе среднего времени
    if i > 0:
        elapsed_time = time.time() - start_time
        average_time_per_screenshot = elapsed_time / i
        remaining_time_seconds = int(
            average_time_per_screenshot * remaining_screenshots)
    else:
        remaining_time_seconds = 0

    # Вывод текущего статуса
    print(f"{current_success_percentage:.0f}%. Снято {i} из {num_screenshots} скриншотов. "
          f"Осталось {remaining_screenshots} скриншотов, примерно {format_time(remaining_time_seconds)}.")

    # Пауза (кроме последней итерации)
    if i < num_screenshots:
        time.sleep(pause_between_shots)

# Итоговый результат
success_percentage = (success_count / num_screenshots) * \
    100 if num_screenshots > 0 else 0
print(
    f"Съемка завершена. Успешно снято {success_count} из {num_screenshots} скриншотов ({success_percentage:.2f}%).")
