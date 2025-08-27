import requests
import subprocess
import os

# Прямые ссылки на установщики
urls = [
    ("PDF24 Creator", "https://download.pdf24.org/pdf24-creator-installer.exe"),
    ("WinRAR", "https://www.win-rar.com/postdownload.html"),
    ("Bitrix24 Desktop", "https://repos.1c-bitrix.ru/b24/bitrix24_desktop_ru.exe"),
    ("VC++ Redistributable x64", "https://aka.ms/vs/17/release/vc_redist.x64.exe"),
    ("VC++ Redistributable x86", "https://aka.ms/vs/17/release/vc_redist.x86.exe")
]

def download_and_install(url, app_name):
    """Загружает и устанавливает приложение."""
    filename = url.split("/")[-1]
    print(f"Скачиваю {app_name}...")
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Установщик {filename} сохранён.")
        
        # Устанавливаем приложение
        print(f"Начинаю установку {app_name}...")
        result = subprocess.run([f"./{filename}", "/silent"], shell=True)
        if result.returncode == 0:
            print(f"{app_name} установлен успешно!")
        else:
            print(f"Установка {app_name} завершилась неудачно.")
        
        # Очищаем временные файлы
        os.remove(filename)
    else:
        print(f"Ошибка при скачивании {app_name}, статус-код: {response.status_code}")

# Проходим по списку программ и выполняем обновление
for app_name, url in urls:
    download_and_install(url, app_name)

print("Все программы обновлены.")
