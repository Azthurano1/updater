import requests
import subprocess
import os
import winreg
import pkg_resources

# Функция для извлечения текущей версии установленного приложения
def get_current_version(app_name):
    try:
        # Пытаемся прочитать DisplayVersion из реестра
        key_path = rf'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{app_name}'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            version_value = winreg.QueryValueEx(key, 'DisplayVersion')[0]
            return version_value
    except FileNotFoundError:
        # Приложение не установлено
        return None

# Функция для получения доступной версии с веб-страницы
def fetch_available_version(url):
    try:
        response = requests.get(url)
        html = response.text
        # Извлекаем версию из текста страницы (простейший пример)
        match = re.search(r'version\s*(\d+\.\d+(?:\.\d+)?)', html)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Ошибка при извлечении версии: {e}")
        return None

# Приложения и их ссылки
apps = [
    ("PDF24 Creator", "https://download.pdf24.org/pdf24-creator-installer.exe"),
    ("WinRAR", "https://www.win-rar.com/postdownload.html"),
    ("Bitrix24 Desktop", "https://repos.1c-bitrix.ru/b24/bitrix24_desktop_ru.exe"),
    ("VC++ Redistributable x64", "https://aka.ms/vs/17/release/vc_redist.x64.exe"),
    ("VC++ Redistributable x86", "https://aka.ms/vs/17/release/vc_redist.x86.exe")
]

# Процедура скачивания и установки
def download_and_install(url, app_name):
    """Загружает и устанавливает приложение"""
    filename = url.split("/")[-1]
    print(f"Скачиваю {app_name}...")
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Файл {filename} сохранён.")
        
        # Запускаем установку
        print(f"Начинаем установку {app_name}...")
        result = subprocess.run([f"./{filename}", "/silent"], shell=True)
        if result.returncode == 0:
            print(f"{app_name} установлен успешно!")
        else:
            print(f"Ошибка при установке {app_name}.")
        
        # Очищаем временные файлы
        os.remove(filename)
    else:
        print(f"Ошибка при скачивании {app_name}, статус-код: {response.status_code}")

# Главная логика обновления
for app_name, url in apps:
    current_version = get_current_version(app_name)
    available_version = fetch_available_version(url)
    
    if current_version is None:
        print(f"{app_name} не установлен. Начинаем установку...")
        download_and_install(url, app_name)
    elif available_version is None:
        print(f"Не удалось определить доступную версию для {app_name}. Пропускаем.")
    elif pkg_resources.parse_version(current_version) < pkg_resources.parse_version(available_version):
        print(f"Обнаружено новое обновление для {app_name} ({current_version} -> {available_version}). Начинаем обновление...")
        download_and_install(url, app_name)
    else:
        print(f"{app_name} уже актуален ({current_version}).")

print("Процесс обновления завершён.")