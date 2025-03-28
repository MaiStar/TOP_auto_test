import os
import time
import urllib.request
import urllib.error

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

# Расчет и вывод времени выполнения
total_time = num_screenshots * 10
print(f"Съемка {num_screenshots} скриншотов займет {total_time} секунд.")

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
