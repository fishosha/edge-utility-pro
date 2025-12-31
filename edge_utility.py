import base64
import hashlib
import json
import secrets
import string
import uuid
from urllib.parse import quote, unquote
import qrcode
from colorama import init, Fore, Style
import pyperclip
import os
import time
import requests
import platform
import socket
from datetime import datetime
import random
import math
import sys

# Инициализация colorama
init(autoreset=True)

# Глобальные настройки
SETTINGS_FILE = "edge_settings.json"
DEFAULT_SETTINGS = {
    "theme": "default",
    "sound": False,
    "autocopy": True,
    "animation": True,
    "language": "ru",
    "developer_mode": False,
    "show_tips": True,
    "log_operations": False
}

def load_settings():
    """Загрузка настроек из файла"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_SETTINGS, **json.load(f)}
        except:
            return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings):
    """Сохранение настроек в файл"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

SETTINGS = load_settings()

# Тема оформления
THEMES = {
    "default": {"header": Fore.YELLOW, "text": Fore.WHITE, "accent": Fore.CYAN, "success": Fore.GREEN, "error": Fore.RED},
    "dark": {"header": Fore.MAGENTA, "text": Fore.WHITE, "accent": Fore.BLUE, "success": Fore.GREEN, "error": Fore.RED},
    "matrix": {"header": Fore.GREEN, "text": Fore.WHITE, "accent": Fore.CYAN, "success": Fore.GREEN, "error": Fore.RED},
    "fire": {"header": Fore.RED, "text": Fore.YELLOW, "accent": Fore.MAGENTA, "success": Fore.GREEN, "error": Fore.RED},
    "ocean": {"header": Fore.BLUE, "text": Fore.CYAN, "accent": Fore.GREEN, "success": Fore.GREEN, "error": Fore.RED}
}

theme = THEMES[SETTINGS["theme"]]

def printc(text, color_type="text"):
    """Печать с цветом из темы"""
    color = theme.get(color_type, Fore.WHITE)
    print(color + text)

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Печать заголовка"""
    clear_screen()
    printc("═" * 70, "header")
    printc(f" {title:^68} ", "header")
    printc("═" * 70, "header")
    print()

def wait_for_enter():
    """Ожидание Enter"""
    printc("\n─" * 60, "accent")
    printc("Нажмите Enter для продолжения...", "header")
    input()

def show_logo():
    """Показать анимированный логотип"""
    clear_screen()
    
    logo_parts = [
        f"""{theme['header']}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║""",
        f"""    ║  ███████╗██████╗  ██████╗ ███████╗    ██╗   ██╗████████╗██╗  ║""",
        f"""    ║  ██╔════╝██╔══██╗██╔════╝ ██╔════╝    ██║   ██║╚══██╔══╝██║  ║""",
        f"""    ║  █████╗  ██║  ██║██║  ███╗█████╗      ██║   ██║   ██║   ██║  ║""",
        f"""    ║  ██╔══╝  ██║  ██║██║   ██║██╔══╝      ██║   ██║   ██║   ██║  ║""",
        f"""    ║  ███████╗██████╔╝╚██████╔╝███████╗    ╚██████╔╝   ██║   ██║  ║""",
        f"""    ║  ╚══════╝╚═════╝  ╚═════╝ ╚══════╝     ╚═════╝    ╚═╝   ╚═╝  ║""",
        f"""    ║                                                              ║""",
        f"""    ║                 EDGE UTILITY PRO v4.0                        ║""",
        f"""    ╚══════════════════════════════════════════════════════════════╝
    """
    ]
    
    for part in logo_parts:
        print(part)
        if SETTINGS["animation"]:
            time.sleep(0.1)
    
    printc("\n" + " " * 15 + "Загрузка системы...", "accent")
    for i in range(1, 101, 5):
        if SETTINGS["animation"]:
            time.sleep(0.02)
        bar = "█" * (i // 2) + "░" * (50 - i // 2)
        print(f"\r{theme['accent']} [{bar}] {i}%", end="")
    
    print(f"\n{theme['success']} ✓ Система готова к работе!")
    time.sleep(0.5)

# ==================== СИСТЕМНЫЕ ФУНКЦИИ ====================

def process_monitor():
    """Монитор процессов"""
    print_header("📊 МОНИТОР ПРОЦЕССОВ")
    
    try:
        import psutil
        
        printc("Сбор информации о процессах...", "accent")
        time.sleep(0.5)
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except:
                pass
        
        # Сортируем по использованию CPU
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        printc(f"\nВсего процессов: {len(processes)}", "header")
        printc(f"{'PID':>6} {'Имя':20} {'CPU %':>6} {'Память %':>9} {'Статус':>10}", "header")
        printc("─" * 60, "header")
        
        for proc in processes[:25]:  # Показываем топ-25
            name = proc['name'][:19] if proc['name'] else 'N/A'
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            status = proc['status'][:9] if proc['status'] else 'N/A'
            
            if cpu > 50:
                cpu_color = theme['error']
            elif cpu > 20:
                cpu_color = theme['accent']
            else:
                cpu_color = theme['text']
            
            if mem > 10:
                mem_color = theme['error']
            elif mem > 5:
                mem_color = theme['accent']
            else:
                mem_color = theme['text']
            
            print(f"{proc['pid']:6} {name:20} {cpu_color}{cpu:6.1f}{Fore.RESET} {mem_color}{mem:9.1f}{Fore.RESET} {status:>10}")
        
        # Системная информация
        printc(f"\n{'═'*60}", "header")
        printc("📈 СИСТЕМНАЯ ИНФОРМАЦИЯ:", "header")
        
        cpu_total = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # CPU информация
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        printc(f"\n💻 ПРОЦЕССОР:", "header")
        printc(f"Загрузка CPU: {cpu_total:.1f}%", 
               "error" if cpu_total > 80 else "accent" if cpu_total > 50 else "text")
        printc(f"Ядер/потоков: {cpu_count}", "text")
        if cpu_freq:
            printc(f"Частота: {cpu_freq.current:.0f} MHz", "text")
        
        # Память
        printc(f"\n💾 ПАМЯТЬ:", "header")
        printc(f"Использовано: {memory.percent:.1f}% ({memory.used//1024//1024:,d} MB)", 
               "error" if memory.percent > 80 else "accent" if memory.percent > 50 else "text")
        printc(f"Всего: {memory.total//1024//1024:,d} MB", "text")
        printc(f"Доступно: {memory.available//1024//1024:,d} MB", "text")
        
        # Диск
        printc(f"\n💿 ДИСК:", "header")
        printc(f"Использовано: {disk.percent:.1f}%", 
               "error" if disk.percent > 90 else "accent" if disk.percent > 70 else "text")
        printc(f"Всего: {disk.total//1024//1024//1024:,d} GB", "text")
        printc(f"Свободно: {disk.free//1024//1024//1024:,d} GB", "text")
        
        # Сеть
        printc(f"\n🌐 СЕТЬ:", "header")
        net_io = psutil.net_io_counters()
        printc(f"Отправлено: {net_io.bytes_sent//1024//1024:,d} MB", "text")
        printc(f"Получено: {net_io.bytes_recv//1024//1024:,d} MB", "text")
        
        # Температура (если доступно)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                printc(f"\n🌡️ ТЕМПЕРАТУРА:", "header")
                for name, entries in temps.items():
                    for entry in entries[:1]:
                        temp_color = "error" if entry.current > 80 else "accent" if entry.current > 60 else "text"
                        printc(f"{name}: {entry.current:.1f}°C", temp_color)
        except:
            pass
        
    except ImportError:
        printc("\n⚠ Для работы монитора процессов установите psutil:", "error")
        printc("pip install psutil", "accent")
        
        # Альтернативная информация о системе
        printc("\n📋 ОСНОВНАЯ ИНФОРМАЦИЯ О СИСТЕМЕ:", "header")
        printc(f"Система: {platform.system()} {platform.release()}", "text")
        printc(f"Процессор: {platform.processor()}", "text")
        printc(f"Архитектура: {platform.architecture()[0]}", "text")
        printc(f"Python: {platform.python_version()}", "text")
    
    wait_for_enter()

def system_info():
    """Информация о системе"""
    print_header("💻 ИНФОРМАЦИЯ О СИСТЕМЕ")
    
    printc("Сбор системной информации...", "accent")
    time.sleep(0.5)
    
    printc(f"\n{'═'*60}", "header")
    printc("🏷️  ОБЩАЯ ИНФОРМАЦИЯ:", "header")
    printc(f"Система: {platform.system()} {platform.release()}", "text")
    printc(f"Версия: {platform.version()}", "text")
    printc(f"Архитектура: {platform.architecture()[0]}", "text")
    printc(f"Имя компьютера: {platform.node()}", "text")
    
    printc(f"\n💻 АППАРАТНОЕ ОБЕСПЕЧЕНИЕ:", "header")
    printc(f"Процессор: {platform.processor()}", "text")
    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
        printc(f"Модель CPU: {cpu_info.get('brand_raw', 'N/A')}", "text")
        printc(f"Частота: {cpu_info.get('hz_actual_friendly', 'N/A')}", "text")
        printc(f"Ядер: {cpu_info.get('count', 'N/A')}", "text")
    except:
        pass
    
    printc(f"\n🐍 PYTHON ИНФОРМАЦИЯ:", "header")
    printc(f"Версия Python: {platform.python_version()}", "text")
    printc(f"Исполняемый файл: {sys.executable}", "text")
    printc(f"Путь к Python: {sys.prefix}", "text")
    
    printc(f"\n📁 СИСТЕМНЫЕ ПУТИ:", "header")
    printc(f"Текущая директория: {os.getcwd()}", "text")
    printc(f"Домашняя директория: {os.path.expanduser('~')}", "text")
    printc(f"Временная директория: {os.environ.get('TEMP', os.environ.get('TMP', 'N/A'))}", "text")
    
    printc(f"\n💾 ДИСКОВОЕ ПРОСТРАНСТВО:", "header")
    try:
        import psutil
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                free_gb = usage.free // (1024**3)
                total_gb = usage.total // (1024**3)
                percent = usage.percent
                
                status_color = "error" if percent > 90 else "accent" if percent > 70 else "text"
                printc(f"{partition.device} ({partition.mountpoint}):", "text")
                printc(f"  Свободно: {free_gb:,d} GB из {total_gb:,d} GB ({percent:.1f}%)", status_color)
            except:
                pass
    except:
        printc("Установите psutil для детальной информации о дисках", "error")
    
    printc(f"\n🌐 СЕТЕВАЯ ИНФОРМАЦИЯ:", "header")
    try:
        hostname = socket.gethostname()
        printc(f"Имя хоста: {hostname}", "text")
        
        # IP адреса
        printc("IP адреса:", "text")
        addrs = []
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == socket.AF_INET:
                    addrs.append(snic.address)
        
        for addr in set(addrs):
            printc(f"  • {addr}", "accent")
    except:
        printc("Не удалось получить сетевую информацию", "error")
    
    wait_for_enter()

def internet_speed_test():
    """Тест скорости интернета"""
    print_header("🌐 ТЕСТ СКОРОСТИ ИНТЕРНЕТА")
    
    printc("Внимание: Тест скорости использует открытые серверы для измерения.", "accent")
    printc("Это может занять несколько секунд...\n", "text")
    
    test_servers = [
        {"name": "Сервер 1", "url": "http://speedtest.ftp.otenet.gr/files/test1Mb.db"},
        {"name": "Сервер 2", "url": "http://ipv4.download.thinkbroadband.com/5MB.zip"},
        {"name": "Сервер 3", "url": "http://proof.ovh.net/files/1Mb.dat"}
    ]
    
    printc("Выберите сервер для теста:", "header")
    for i, server in enumerate(test_servers, 1):
        printc(f"{i}. {server['name']}", "text")
    
    try:
        choice = int(input(f"\n{theme['accent']}Выбор (1-{len(test_servers)}): {theme['text']}")) - 1
        
        if 0 <= choice < len(test_servers):
            server = test_servers[choice]
            printc(f"\nТестирование через {server['name']}...", "accent")
            
            # Тест скорости загрузки
            printc("\n📥 Тестирование скорости загрузки...", "header")
            
            start_time = time.time()
            try:
                response = requests.get(server['url'], stream=True, timeout=10)
                response.raise_for_status()
                
                total_size = 0
                chunk_size = 1024 * 1024  # 1 MB
                
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        total_size += len(chunk)
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        speed = total_size / elapsed / 1024 / 1024  # MB/s
                        print(f"\rСкачано: {total_size/1024/1024:.2f} MB | Скорость: {speed:.2f} MB/s", end="")
                    
                    if elapsed > 5:  # Тестируем 5 секунд
                        break
                
                download_speed = total_size / elapsed / 1024 / 1024  # MB/s
                printc(f"\n\n📥 Результат загрузки: {download_speed:.2f} MB/s", "success")
                
                # Оценка скорости
                if download_speed > 50:
                    rating = "Отлично! 🚀"
                    color = "success"
                elif download_speed > 20:
                    rating = "Хорошо! 👍"
                    color = "accent"
                elif download_speed > 5:
                    rating = "Нормально 👌"
                    color = "text"
                else:
                    rating = "Медленно 🐢"
                    color = "error"
                
                printc(f"Оценка: {rating}", color)
                
                # Примерная скорость в Мбит/с
                mbps = download_speed * 8
                printc(f"Примерно: {mbps:.0f} Мбит/с", "text")
                
                # Что можно делать с такой скоростью
                printc(f"\n🎯 Возможности при такой скорости:", "header")
                if mbps > 100:
                    printc("• 4K видео поток", "success")
                    printc("• Онлайн игры без лагов", "success")
                    printc("• Быстрая загрузка файлов", "success")
                elif mbps > 50:
                    printc("• Full HD видео", "accent")
                    printc("• Видеозвонки HD", "accent")
                    printc("• Комфортный веб-сёрфинг", "accent")
                elif mbps > 20:
                    printc("• HD видео", "text")
                    printc("• Аудио поток", "text")
                    printc("• Работа с облаками", "text")
                else:
                    printc("• Базовый веб-сёрфинг", "error")
                    printc("• Электронная почта", "error")
                    printc("• Медленная загрузка", "error")
                
            except Exception as e:
                printc(f"\n✗ Ошибка тестирования: {e}", "error")
                
                # Симуляция теста для демонстрации
                printc("\nЗапуск демо-теста...", "accent")
                download_speed = random.uniform(10, 100)
                printc(f"Демо-скорость: {download_speed:.2f} MB/s", "success")
        
        else:
            printc("Неверный выбор!", "error")
    
    except ValueError:
        printc("Неверный ввод!", "error")
    
    wait_for_enter()

# ==================== НОВЫЕ ФИШКИ ====================

def text_to_emoji():
    """Конвертер текста в эмодзи"""
    print_header("😊 КОНВЕРТЕР ТЕКСТА В ЭМОДЗИ")
    
    text = input(f"{theme['accent']}Введите текст для преобразования:\n{theme['text']}")
    
    if not text.strip():
        printc("Текст не может быть пустым!", "error")
        wait_for_enter()
        return
    
    # Словарь замен
    emoji_dict = {
        'смайл': '😊', 'улыбка': '😄', 'смех': '😂', 'подмиг': '😉',
        'сердце': '❤️', 'любовь': '💖', 'звезда': '⭐', 'огонь': '🔥',
        'молния': '⚡', 'снег': '❄️', 'солнце': '☀️', 'луна': '🌙',
        'облако': '☁️', 'дождь': '🌧️', 'гроза': '⛈️', 'радуга': '🌈',
        'кофе': '☕', 'чай': '🍵', 'пицца': '🍕', 'бургер': '🍔',
        'торт': '🎂', 'мороженое': '🍦', 'пиво': '🍺', 'вино': '🍷',
        'музыка': '🎵', 'гитара': '🎸', 'ноты': '🎶', 'фильм': '🎬',
        'камера': '📷', 'телефон': '📱', 'компьютер': '💻', 'книга': '📚',
        'письмо': '✉️', 'карандаш': '✏️', 'ключ': '🔑', 'часы': '⏰',
        'деньги': '💰', 'банк': '🏦', 'машина': '🚗', 'самолет': '✈️',
        'корабль': '🚢', 'поезд': '🚂', 'дом': '🏠', 'офис': '🏢',
        'больница': '🏥', 'школа': '🏫', 'университет': '🎓', 'работа': '💼',
        'спорт': '⚽', 'футбол': '⚽', 'баскетбол': '🏀', 'теннис': '🎾',
        'плавание': '🏊', 'бег': '🏃', 'йога': '🧘', 'медитация': '🧘‍♂️',
        'здоровье': '💪', 'болезнь': '🤒', 'доктор': '👨‍⚕️', 'медсестра': '👩‍⚕️',
        'учитель': '👨‍🏫', 'студент': '👨‍🎓', 'программист': '👨‍💻', 'дизайнер': '👨‍🎨',
        'хорошо': '👍', 'плохо': '👎', 'ок': '👌', 'привет': '👋',
        'пока': '👋', 'спасибо': '🙏', 'пожалуйста': '🙏', 'извини': '😔',
        'поздравляю': '🎉', 'день рождения': '🎂', 'новый год': '🎄',
        'рождество': '🎅', 'халлоуин': '🎃', 'пасха': '🐰', 'отпуск': '🏖️',
        'пляж': '🏖️', 'море': '🌊', 'горы': '⛰️', 'лес': '🌲',
        'цветок': '🌸', 'дерево': '🌳', 'животное': '🐾', 'кошка': '🐱',
        'собака': '🐶', 'птица': '🐦', 'рыба': '🐟', 'лев': '🦁',
        'тигр': '🐯', 'медведь': '🐻', 'заяц': '🐰', 'волк': '🐺',
        'сова': '🦉', 'дельфин': '🐬', 'кит': '🐋', 'акула': '🦈',
        'змея': '🐍', 'ящерица': '🦎', 'паук': '🕷️', 'бабочка': '🦋',
        'пчела': '🐝', 'муравей': '🐜', 'улитка': '🐌', 'червяк': '🐛'
    }
    
    # Преобразование текста
    words = text.lower().split()
    result = []
    
    for word in words:
        # Проверяем слово целиком
        if word in emoji_dict:
            result.append(emoji_dict[word])
        else:
            # Проверяем часть слова
            found = False
            for key, emoji in emoji_dict.items():
                if key in word:
                    result.append(emoji)
                    found = True
                    break
            if not found:
                result.append(word)
    
    converted = ' '.join(result)
    
    printc(f"\n🎭 Преобразованный текст:", "success")
    printc(converted, "accent")
    
    if SETTINGS["autocopy"]:
        pyperclip.copy(converted)
        printc("✓ Скопировано в буфер", "success")
    
    wait_for_enter()

def color_palette_generator():
    """Генератор цветовых палитр"""
    print_header("🎨 ГЕНЕРАТОР ЦВЕТОВЫХ ПАЛИТР")
    
    printc("Выберите тип палитры:", "header")
    printc("1. Аналогичные цвета", "text")
    printc("2. Контрастные цвета", "text")
    printc("3. Теплые цвета", "text")
    printc("4. Холодные цвета", "text")
    printc("5. Пастельные цвета", "text")
    printc("6. Яркие цвета", "text")
    printc("7. Монохромная палитра", "text")
    
    try:
        choice = int(input(f"\n{theme['accent']}Выбор (1-7): {theme['text']}"))
        
        printc("\nГенерация палитры...", "accent")
        time.sleep(0.5)
        
        colors = []
        
        if choice == 1:  # Аналогичные
            base_hue = random.randint(0, 360)
            for i in range(5):
                hue = (base_hue + random.randint(-30, 30)) % 360
                saturation = random.randint(60, 90)
                lightness = random.randint(40, 70)
                colors.append((hue, saturation, lightness))
                
        elif choice == 2:  # Контрастные
            base_hue = random.randint(0, 360)
            for i in range(5):
                hue = (base_hue + i * 72) % 360  # Разделение цветового круга
                saturation = random.randint(70, 100)
                lightness = random.randint(40, 60)
                colors.append((hue, saturation, lightness))
                
        elif choice == 3:  # Теплые
            for i in range(5):
                hue = random.randint(0, 60)  # Красные, оранжевые, желтые
                saturation = random.randint(70, 100)
                lightness = random.randint(40, 70)
                colors.append((hue, saturation, lightness))
                
        elif choice == 4:  # Холодные
            for i in range(5):
                hue = random.randint(180, 300)  # Синие, фиолетовые
                saturation = random.randint(70, 100)
                lightness = random.randint(40, 70)
                colors.append((hue, saturation, lightness))
                
        elif choice == 5:  # Пастельные
            for i in range(5):
                hue = random.randint(0, 360)
                saturation = random.randint(20, 50)
                lightness = random.randint(70, 90)
                colors.append((hue, saturation, lightness))
                
        elif choice == 6:  # Яркие
            for i in range(5):
                hue = random.randint(0, 360)
                saturation = 100
                lightness = random.randint(40, 60)
                colors.append((hue, saturation, lightness))
                
        elif choice == 7:  # Монохромная
            base_hue = random.randint(0, 360)
            for i in range(5):
                hue = base_hue
                saturation = random.randint(30, 80)
                lightness = 20 + i * 15
                colors.append((hue, saturation, lightness))
        
        else:
            printc("Неверный выбор!", "error")
            wait_for_enter()
            return
        
        # Функция для преобразования HSL в HEX
        def hsl_to_hex(h, s, l):
            h /= 360
            s /= 100
            l /= 100
            
            if s == 0:
                r = g = b = l
            else:
                def hue_to_rgb(p, q, t):
                    if t < 0: t += 1
                    if t > 1: t -= 1
                    if t < 1/6: return p + (q - p) * 6 * t
                    if t < 1/2: return q
                    if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                    return p
                
                q = l * (1 + s) if l < 0.5 else l + s - l * s
                p = 2 * l - q
                
                r = hue_to_rgb(p, q, h + 1/3)
                g = hue_to_rgb(p, q, h)
                b = hue_to_rgb(p, q, h - 1/3)
            
            r = int(round(r * 255))
            g = int(round(g * 255))
            b = int(round(b * 255))
            
            return f"#{r:02x}{g:02x}{b:02x}".upper()
        
        # Отображение палитры
        printc(f"\n🎨 Сгенерированная палитра:", "success")
        print()
        
        for i, (h, s, l) in enumerate(colors, 1):
            hex_color = hsl_to_hex(h, s, l)
            rgb_color = f"RGB({int(h/360*255)}, {int(s/100*255)}, {int(l/100*255)})"
            hsl_color = f"HSL({int(h)}, {int(s)}%, {int(l)}%)"
            
            # Создаем цветной блок в консоли (простая эмуляция)
            block = "███" * 10
            print(f"{theme['accent']}Цвет {i}:")
            print(f"{theme['text']}  HEX: {hex_color}")
            print(f"{theme['text']}  {rgb_color}")
            print(f"{theme['text']}  {hsl_color}")
            print()
        
        # Сохранение палитры
        save = input(f"{theme['accent']}Сохранить палитру? (y/n): {theme['text']}").lower()
        if save == 'y':
            filename = f"palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Цветовая палитра\n")
                f.write("=" * 50 + "\n")
                for i, (h, s, l) in enumerate(colors, 1):
                    hex_color = hsl_to_hex(h, s, l)
                    f.write(f"\nЦвет {i}:\n")
                    f.write(f"HEX: {hex_color}\n")
                    f.write(f"HSL: {int(h)}, {int(s)}%, {int(l)}%\n")
            
            printc(f"✓ Палитра сохранена как {filename}", "success")
    
    except ValueError:
        printc("Неверный ввод!", "error")
    
    wait_for_enter()

def ascii_art_generator():
    """Генератор ASCII арта"""
    print_header("🖼️ ГЕНЕРАТОР ASCII АРТА")
    
    printc("Выберите тип ASCII арта:", "header")
    printc("1. Текст в ASCII", "text")
    printc("2. Геометрические фигуры", "text")
    printc("3. Случайный паттерн", "text")
    printc("4. Кастомный текст", "text")
    
    try:
        choice = int(input(f"\n{theme['accent']}Выбор (1-4): {theme['text']}"))
        
        printc("\nСоздание ASCII арта...", "accent")
        time.sleep(0.5)
        
        ascii_art = ""
        
        if choice == 1:  # Текст в ASCII
            fonts = [
                """        
  ___                  _   
 | __|_ __  ___ __ _ _| |_ 
 | _|| '  \/ -_) _` |_   _|
 |___|_|_|_\___\__,_| |_|  
                """,
                """
  ███████╗███████╗███████╗
  ██╔════╝██╔════╝██╔════╝
  █████╗  █████╗  █████╗  
  ██╔══╝  ██╔══╝  ██╔══╝  
  ███████╗███████╗███████╗
  ╚══════╝╚══════╝╚══════╝
                """,
                """
  ╔═══╗╔═══╗╔═══╗
  ║╔═╗║║╔═╗║║╔═╗║
  ║╚══╗║║ ║║║║ ╚╝
  ╚══╗║║║ ║║║║╔═╗
  ║╚═╝║║╚═╝║║╚╩═║
  ╚═══╝╚═══╝╚═══╝
                """
            ]
            
            ascii_art = random.choice(fonts)
            printc("\nASCII текст:", "success")
            
        elif choice == 2:  # Геометрические фигуры
            shapes = [
                """
        ╔════════════════════╗
        ║                    ║
        ║       КРУГ         ║
        ║                    ║
        ╚════════════════════╝
                """,
                """
           /\\
          /  \\
         /    \\
        /______\\
                ТРЕУГОЛЬНИК
                """,
                """
        ████████████████████
        ██                ██
        ██    КВАДРАТ     ██
        ██                ██
        ████████████████████
                """
            ]
            
            ascii_art = random.choice(shapes)
            printc("\nГеометрическая фигура:", "success")
            
        elif choice == 3:  # Случайный паттерн
            width = 40
            height = 10
            symbols = ["█", "▓", "▒", "░", "◼", "◻", "○", "●", "◇", "◆"]
            
            for y in range(height):
                line = ""
                for x in range(width):
                    if random.random() > 0.3:
                        line += random.choice(symbols)
                    else:
                        line += " "
                ascii_art += line + "\n"
            
            printc("\nСлучайный паттерн:", "success")
            
        elif choice == 4:  # Кастомный текст
            text = input(f"{theme['accent']}Введите текст для ASCII арта: {theme['text']}")
            
            if not text.strip():
                printc("Текст не может быть пустым!", "error")
                wait_for_enter()
                return
            
            # Простой ASCII арт из текста
            border = "═" * (len(text) + 4)
            ascii_art = f"""
    ╔{border}╗
    ║  {text.upper()}  ║
    ╚{border}╝
            """
            
            printc("\nКастомный ASCII арт:", "success")
        
        else:
            printc("Неверный выбор!", "error")
            wait_for_enter()
            return
        
        # Вывод ASCII арта
        print(ascii_art)
        
        # Сохранение
        save = input(f"\n{theme['accent']}Сохранить ASCII арт? (y/n): {theme['text']}").lower()
        if save == 'y':
            filename = f"ascii_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(ascii_art)
            
            printc(f"✓ ASCII арт сохранен как {filename}", "success")
    
    except ValueError:
        printc("Неверный ввод!", "error")
    
    wait_for_enter()

def file_info():
    """Информация о файле"""
    print_header("📄 ИНФОРМАЦИЯ О ФАЙЛЕ")
    
    filepath = input(f"{theme['accent']}Введите путь к файлу: {theme['text']}")
    
    if not os.path.exists(filepath):
        printc("Файл не найден!", "error")
        wait_for_enter()
        return
    
    try:
        stats = os.stat(filepath)
        
        printc("\n📊 ИНФОРМАЦИЯ О ФАЙЛЕ:", "success")
        printc(f"Имя файла: {os.path.basename(filepath)}", "text")
        printc(f"Путь: {os.path.dirname(filepath)}", "text")
        printc(f"Полный путь: {os.path.abspath(filepath)}", "text")
        
        # Размер файла
        size = stats.st_size
        size_str = ""
        if size < 1024:
            size_str = f"{size} байт"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.2f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size/1024/1024:.2f} MB"
        else:
            size_str = f"{size/1024/1024/1024:.2f} GB"
        
        printc(f"Размер: {size_str}", "text")
        
        # Даты
        printc(f"\n📅 ДАТЫ:", "header")
        printc(f"Создан: {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}", "text")
        printc(f"Изменен: {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}", "text")
        printc(f"Открыт: {datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')}", "text")
        
        # Разрешения
        printc(f"\n🔒 ПРАВА ДОСТУПА:", "header")
        mode = stats.st_mode
        permissions = ""
        
        # Владелец
        permissions += "r" if mode & 0o400 else "-"
        permissions += "w" if mode & 0o200 else "-"
        permissions += "x" if mode & 0o100 else "-"
        
        # Группа
        permissions += "r" if mode & 0o040 else "-"
        permissions += "w" if mode & 0o020 else "-"
        permissions += "x" if mode & 0o010 else "-"
        
        # Остальные
        permissions += "r" if mode & 0o004 else "-"
        permissions += "w" if mode & 0o002 else "-"
        permissions += "x" if mode & 0o001 else "-"
        
        printc(f"Права: {permissions}", "text")
        
        # Тип файла
        printc(f"\n📁 ТИП ФАЙЛА:", "header")
        if os.path.isfile(filepath):
            printc("Тип: Обычный файл", "text")
            ext = os.path.splitext(filepath)[1].lower()
            printc(f"Расширение: {ext if ext else 'Нет'}", "text")
        elif os.path.isdir(filepath):
            printc("Тип: Директория", "text")
        elif os.path.islink(filepath):
            printc("Тип: Символическая ссылка", "text")
        
        # Хеш файла
        printc(f"\n🔐 ХЕШ ФАЙЛА:", "header")
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                md5 = hashlib.md5(content).hexdigest()
                sha256 = hashlib.sha256(content).hexdigest()
                
                printc(f"MD5: {md5}", "text")
                printc(f"SHA-256: {sha256}", "text")
                
                if SETTINGS["autocopy"]:
                    pyperclip.copy(sha256)
                    printc("✓ SHA-256 скопирован в буфер", "success")
        except Exception as e:
            printc(f"Не удалось вычислить хеш: {e}", "error")
        
        # Дополнительная информация
        printc(f"\n📈 СТАТИСТИКА:", "header")
        try:
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    printc(f"Количество строк: {len(lines)}", "text")
                    
                    # Подсчет слов и символов
                    text = ''.join(lines)
                    words = len(text.split())
                    chars = len(text)
                    printc(f"Количество слов: {words:,d}", "text")
                    printc(f"Количество символов: {chars:,d}", "text")
        except:
            pass
        
    except Exception as e:
        printc(f"Ошибка: {e}", "error")
    
    wait_for_enter()

# ==================== БАЗОВЫЕ ФУНКЦИИ ====================

def base64_tool():
    """Base64 кодирование/декодирование"""
    print_header("BASE64 КОДИРОВАНИЕ/ДЕКОДИРОВАНИЕ")
    
    text = input(f"{theme['accent']}Введите текст для кодирования/декодирования:\n{theme['text']}")
    
    if not text.strip():
        printc("Текст не может быть пустым!", "error")
        wait_for_enter()
        return
    
    printc("\nВыберите действие:", "header")
    printc("1. Кодировать в Base64", "text")
    printc("2. Декодировать из Base64", "text")
    
    choice = input(f"{theme['accent']}Выбор: {theme['text']}")
    
    try:
        if choice == '1':
            result = base64.b64encode(text.encode()).decode()
            printc(f"\n✓ Закодированный текст:", "success")
        elif choice == '2':
            result = base64.b64decode(text).decode()
            printc(f"\n✓ Декодированный текст:", "success")
        else:
            printc("Неверный выбор!", "error")
            wait_for_enter()
            return
        
        printc(result, "accent")
        
        if SETTINGS["autocopy"]:
            pyperclip.copy(result)
            printc("✓ Скопировано в буфер", "success")
        
    except Exception as e:
        printc(f"✗ Ошибка: {e}", "error")
    
    wait_for_enter()

def hash_generator():
    """Генератор хешей"""
    print_header("🔑 ГЕНЕРАТОР ХЕШЕЙ")
    
    text = input(f"{theme['accent']}Введите текст для хеширования:\n{theme['text']}")
    
    if not text.strip():
        printc("Текст не может быть пустым!", "error")
        wait_for_enter()
        return
    
    algorithms = [
        ("MD5", hashlib.md5),
        ("SHA-1", hashlib.sha1),
        ("SHA-256", hashlib.sha256),
        ("SHA-512", hashlib.sha512),
        ("SHA3-256", hashlib.sha3_256),
        ("SHA3-512", hashlib.sha3_512),
        ("BLAKE2b", hashlib.blake2b),
        ("BLAKE2s", hashlib.blake2s)
    ]
    
    printc("\nРезультаты хеширования:", "header")
    for name, algo in algorithms:
        try:
            hash_obj = algo(text.encode())
            result = hash_obj.hexdigest()
            printc(f"\n{name}:", "accent")
            printc(f"{result}", "text")
        except:
            printc(f"{name}: Не поддерживается", "error")
    
    if SETTINGS["autocopy"]:
        pyperclip.copy(result)
        printc("\n✓ Последний хеш скопирован в буфер", "success")
    
    wait_for_enter()

def qr_generator():
    """Генератор QR-кодов"""
    print_header("📱 ГЕНЕРАТОР QR-КОДОВ")
    
    text = input(f"{theme['accent']}Введите текст или URL для QR-кода:\n{theme['text']}")
    
    if not text.strip():
        printc("Текст не может быть пустым!", "error")
        wait_for_enter()
        return
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        printc("\n✓ QR-код создан (ASCII представление):", "success")
        
        matrix = qr.get_matrix()
        for row in matrix:
            line = ''.join(['██' if cell else '  ' for cell in row])
            printc(line, "text")
        
        printc(f"\nИнформация:", "header")
        printc(f"Размер: {len(matrix)}x{len(matrix)}", "text")
        printc(f"Длина данных: {len(text)} символов", "text")
        
        save = input(f"\n{theme['accent']}Сохранить как PNG? (y/n): {theme['text']}").lower()
        if save == 'y':
            filename = f"qr_{int(time.time())}.png"
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            printc(f"✓ Сохранено как {filename}", "success")
        
    except Exception as e:
        printc(f"✗ Ошибка: {e}", "error")
    
    wait_for_enter()

def url_tools():
    """Инструменты для работы с URL"""
    print_header("🌐 URL ИНСТРУМЕНТЫ")
    
    printc("Выберите действие:", "header")
    printc("1. URL encode", "text")
    printc("2. URL decode", "text")
    
    choice = input(f"\n{theme['accent']}Выбор: {theme['text']}")
    
    if choice == '1':
        text = input(f"{theme['accent']}Введите текст для кодирования:\n{theme['text']}")
        encoded = quote(text)
        printc(f"\n✓ Закодированный URL:", "success")
        printc(encoded, "accent")
        
    elif choice == '2':
        text = input(f"{theme['accent']}Введите URL для декодирования:\n{theme['text']}")
        decoded = unquote(text)
        printc(f"\n✓ Декодированный текст:", "success")
        printc(decoded, "accent")
    
    else:
        printc("Неверный выбор!", "error")
    
    if SETTINGS["autocopy"] and choice in ['1', '2']:
        pyperclip.copy(encoded if choice == '1' else decoded)
        printc("\n✓ Скопировано в буфер", "success")
    
    wait_for_enter()

def password_generator():
    """Генератор безопасных паролей"""
    print_header("🔐 ГЕНЕРАТОР ПАРОЛЕЙ")
    
    try:
        length = int(input(f"{theme['accent']}Длина пароля (8-64): {theme['text']}") or 16)
        length = max(8, min(64, length))
        
        printc("\nИспользовать символы:", "header")
        printc("1. Только буквы и цифры", "text")
        printc("2. Буквы, цифры и специальные символы", "text")
        printc("3. Только буквы", "text")
        printc("4. Только цифры", "text")
        printc("5. Произвольный набор", "text")
        
        choice = input(f"\n{theme['accent']}Выбор: {theme['text']}")
        
        if choice == '1':
            chars = string.ascii_letters + string.digits
        elif choice == '2':
            chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        elif choice == '3':
            chars = string.ascii_letters
        elif choice == '4':
            chars = string.digits
        elif choice == '5':
            custom = input(f"{theme['accent']}Введите свои символы: {theme['text']}")
            chars = custom if custom else string.ascii_letters + string.digits
        else:
            chars = string.ascii_letters + string.digits
        
        # Генерация пароля
        printc("\nГенерация...", "accent")
        time.sleep(0.5)
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        printc(f"\n✅ Сгенерирован пароль:", "success")
        printc(f"{password}", "accent")
        
        # Оценка сложности
        printc("\n📊 Анализ пароля:", "header")
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        printc(f"Длина: {len(password)} символов", "text")
        printc(f"Заглавные буквы: {'✓' if has_upper else '✗'}", "success" if has_upper else "error")
        printc(f"Строчные буквы: {'✓' if has_lower else '✗'}", "success" if has_lower else "error")
        printc(f"Цифры: {'✓' if has_digit else '✗'}", "success" if has_digit else "error")
        printc(f"Спецсимволы: {'✓' if has_special else '✗'}", "success" if has_special else "error")
        
        # Оценка энтропии
        charset_size = len(chars)
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        printc(f"\n🔐 Энтропия: {entropy:.1f} бит", "text")
        
        if entropy > 100:
            printc("Оценка: Отличный пароль! 🎉", "success")
        elif entropy > 60:
            printc("Оценка: Хороший пароль 👍", "accent")
        else:
            printc("Оценка: Слабый пароль 😔", "error")
        
        # Копирование в буфер
        pyperclip.copy(password)
        printc("\n✓ Пароль скопирован в буфер обмена", "success")
        
        # Генерация нескольких вариантов
        printc(f"\n{theme['header']}Дополнительные варианты:", "header")
        for i in range(3):
            alt_password = ''.join(secrets.choice(chars) for _ in range(length))
            printc(f"{i+1}. {alt_password}", "text")
        
    except ValueError:
        printc("Неверный формат длины!", "error")
    
    wait_for_enter()

def text_analyzer():
    """Анализатор текста"""
    print_header("📊 АНАЛИЗАТОР ТЕКСТА")
    
    text = input(f"{theme['accent']}Введите текст для анализа:\n{theme['text']}")
    
    if not text.strip():
        printc("Текст не может быть пустым!", "error")
        wait_for_enter()
        return
    
    printc("\n📊 Результаты анализа:", "header")
    
    # Базовая статистика
    length = len(text)
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    printc(f"Длина текста: {length} символов", "text")
    printc(f"Количество слов: {len(words)}", "text")
    printc(f"Количество предложений: {sentences}", "text")
    if words:
        printc(f"Средняя длина слова: {sum(len(w) for w in words)/len(words):.1f} символов", "text")
    
    # Частота символов
    printc(f"\n📈 Частота символов (топ-10):", "header")
    char_count = {}
    for char in text.lower():
        if char.isalpha():
            char_count[char] = char_count.get(char, 0) + 1
    
    sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for char, count in sorted_chars:
        percentage = (count / length * 100) if length > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        printc(f"  {char}: {count:3} ({percentage:5.1f}%) {bar}", "accent")
    
    wait_for_enter()

def json_formatter():
    """Форматировщик JSON"""
    print_header("📝 JSON ФОРМАТИРОВЩИК")
    
    printc("Выберите действие:", "header")
    printc("1. Форматировать JSON", "text")
    printc("2. Минифицировать JSON", "text")
    printc("3. Проверить JSON", "text")
    
    choice = input(f"\n{theme['accent']}Выбор: {theme['text']}")
    
    if choice not in ['1', '2', '3']:
        printc("Неверный выбор!", "error")
        wait_for_enter()
        return
    
    printc("\nВведите JSON (Ctrl+Z или Ctrl+D для завершения):", "accent")
    printc("(можно вставить многострочный JSON)", "text")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    json_text = '\n'.join(lines)
    
    if not json_text.strip():
        printc("JSON не может быть пустым!", "error")
        wait_for_enter()
        return
    
    try:
        data = json.loads(json_text)
        
        if choice == '1':
            result = json.dumps(data, indent=2, ensure_ascii=False)
            printc(f"\n✓ Отформатированный JSON:", "success")
            printc(result, "text")
            
        elif choice == '2':
            result = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            printc(f"\n✓ Минифицированный JSON:", "success")
            printc(f"Длина: {len(result)} символов", "text")
            printc(result, "text")
            
        elif choice == '3':
            printc(f"\n✅ JSON корректен!", "success")
            printc(f"Тип корневого элемента: {type(data).__name__}", "text")
            
            if isinstance(data, dict):
                printc(f"Ключей: {len(data)}", "text")
                printc("Первые 5 ключей:", "header")
                for i, key in enumerate(list(data.keys())[:5]):
                    printc(f"  {key}", "accent")
            elif isinstance(data, list):
                printc(f"Элементов: {len(data)}", "text")
        
        if SETTINGS["autocopy"] and choice in ['1', '2']:
            pyperclip.copy(result)
            printc("\n✓ Скопировано в буфер", "success")
            
    except json.JSONDecodeError as e:
        printc(f"\n✗ Ошибка в JSON:", "error")
        printc(f"Строка {e.lineno}, столбец {e.colno}: {e.msg}", "error")
        if hasattr(e, 'pos'):
            start = max(0, e.pos - 20)
            end = min(len(e.doc), e.pos + 20)
            printc(f"Часть: {e.doc[start:end]}", "text")
    
    wait_for_enter()

def settings_menu():
    """Меню настроек"""
    global SETTINGS, theme
    
    while True:
        print_header("⚙️ НАСТРОЙКИ")
        
        printc(f"Текущая тема: {SETTINGS['theme']}", "header")
        printc(f"Автокопирование: {'ВКЛ' if SETTINGS['autocopy'] else 'ВЫКЛ'}", "text")
        printc(f"Анимации: {'ВКЛ' if SETTINGS['animation'] else 'ВЫКЛ'}", "text")
        printc(f"Подсказки: {'ВКЛ' if SETTINGS['show_tips'] else 'ВЫКЛ'}", "text")
        printc(f"Режим разработчика: {'ВКЛ' if SETTINGS['developer_mode'] else 'ВЫКЛ'}", "text")
        printc(f"Логирование: {'ВКЛ' if SETTINGS['log_operations'] else 'ВЫКЛ'}", "text")
        
        printc("\nВыберите действие:", "header")
        printc("1. Сменить тему оформления", "text")
        printc("2. Вкл/Выкл автокопирование", "text")
        printc("3. Вкл/Выкл анимации", "text")
        printc("4. Вкл/Выкл подсказки", "text")
        printc("5. Режим разработчика", "text")
        printc("6. Логирование операций", "text")
        printc("7. Сбросить настройки", "error")
        printc("8. Сохранить и выйти", "success")
        printc("q. Выход без сохранения", "text")
        
        choice = input(f"\n{theme['accent']}Выбор: {theme['text']}").lower()
        
        if choice == 'q':
            clear_screen()
            return
        
        if choice == '1':
            printc("\nДоступные темы:", "header")
            for i, theme_name in enumerate(THEMES.keys(), 1):
                printc(f"{i}. {theme_name}", "text")
            
            theme_choice = input(f"\n{theme['accent']}Выберите тему (1-{len(THEMES)}): {theme['text']}")
            try:
                theme_names = list(THEMES.keys())
                selected = theme_names[int(theme_choice) - 1]
                SETTINGS["theme"] = selected
                theme = THEMES[selected]
                printc(f"✓ Тема изменена на {selected}", "success")
            except:
                printc("Неверный выбор!", "error")
        
        elif choice == '2':
            SETTINGS["autocopy"] = not SETTINGS["autocopy"]
            printc(f"Автокопирование: {'ВКЛ' if SETTINGS['autocopy'] else 'ВЫКЛ'}", "success")
        
        elif choice == '3':
            SETTINGS["animation"] = not SETTINGS["animation"]
            printc(f"Анимации: {'ВКЛ' if SETTINGS['animation'] else 'ВЫКЛ'}", "success")
        
        elif choice == '4':
            SETTINGS["show_tips"] = not SETTINGS["show_tips"]
            printc(f"Подсказки: {'ВКЛ' if SETTINGS['show_tips'] else 'ВЫКЛ'}", "success")
        
        elif choice == '5':
            SETTINGS["developer_mode"] = not SETTINGS["developer_mode"]
            printc(f"Режим разработчика: {'ВКЛ' if SETTINGS['developer_mode'] else 'ВЫКЛ'}", "success")
        
        elif choice == '6':
            SETTINGS["log_operations"] = not SETTINGS["log_operations"]
            printc(f"Логирование: {'ВКЛ' if SETTINGS['log_operations'] else 'ВЫКЛ'}", "success")
        
        elif choice == '7':
            confirm = input(f"{theme['accent']}Точно сбросить? (yes/no): {theme['text']}")
            if confirm.lower() == 'yes':
                SETTINGS = DEFAULT_SETTINGS.copy()
                theme = THEMES[SETTINGS["theme"]]
                printc("✓ Настройки сброшены", "success")
        
        elif choice == '8':
            save_settings(SETTINGS)
            printc("✓ Настройки сохранены", "success")
            time.sleep(1)
            clear_screen()
            return
        
        time.sleep(0.5)

# ==================== ГЛАВНОЕ МЕНЮ ====================

def show_menu():
    """Показать главное меню"""
    clear_screen()
    
    printc("═" * 70, "header")
    printc(" " * 10 + "EDGE UTILITY PRO - ПРОФЕССИОНАЛЬНЫЕ ИНСТРУМЕНТЫ", "header")
    printc("═" * 70, "header")
    
    printc("\n📦 ОСНОВНЫЕ ИНСТРУМЕНТЫ:", "header")
    printc("  1. Base64 кодирование/декодирование", "text")
    printc("  2. Генератор хешей", "text")
    printc("  3. QR-код генератор", "text")
    printc("  4. URL инструменты", "text")
    printc("  5. Генератор паролей", "text")
    
    printc("\n📊 АНАЛИЗ ДАННЫХ:", "header")
    printc("  6. Анализатор текста", "text")
    printc("  7. JSON форматировщик", "text")
    printc("  8. Информация о файле", "text")
    
    printc("\n💻 СИСТЕМНЫЕ ИНСТРУМЕНТЫ:", "header")
    printc("  9. Монитор процессов", "text")
    printc(" 10. Информация о системе", "text")
    printc(" 11. Тест скорости интернета", "text")
    
    printc("\n🎨 КРЕАТИВНЫЕ ИНСТРУМЕНТЫ:", "header")
    printc(" 12. Текст в эмодзи", "text")
    printc(" 13. Генератор цветовых палитр", "text")
    printc(" 14. Генератор ASCII арта", "text")
    
    printc("\n⚙️  СИСТЕМА:", "header")
    printc(" 15. Настройки программы", "text")
    
    printc("\n" + "═" * 70, "header")
    printc(" 0. Выход | 99. О программе", "header")
    printc("═" * 70, "header")
    
    return input(f"\n{theme['accent']}Выберите функцию (0-15): {theme['text']}")

def about_program():
    """О программе"""
    print_header("ℹ️ О ПРОГРАММЕ")
    
    info = f"""
{theme['header']}EDGE UTILITY PRO v4.0{theme['text']}

Мощный набор инструментов для разработчиков и IT-специалистов.

{theme['header']}Возможности:{theme['text']}
• Кодирование/декодирование Base64
• Генерация хешей (MD5, SHA, BLAKE2)
• Работа с QR-кодами
• URL кодирование/декодирование
• Генератор безопасных паролей
• Анализатор текста и JSON
• Мониторинг процессов и системы
• Тест скорости интернета
• Конвертер текста в эмодзи
• Генератор цветовых палитр
• Создание ASCII арта
• Анализ информации о файлах

{theme['header']}Системные требования:{theme['text']}
• Python 3.6+
• Windows/Linux/Mac OS
• 50 MB свободного места

{theme['header']}Установленные библиотеки:{theme['text']}
• colorama - цветной вывод
• pyperclip - работа с буфером
• requests - HTTP запросы
• qrcode - генерация QR-кодов
• psutil - мониторинг системы

{theme['header']}Разработчик:{theme['text']}
• Created with ❤️ for IT community
• Версия: 4.0 (Stable)
• Дата сборки: {datetime.now().strftime('%Y-%m-%d')}

{theme['success']}100% безопасный код для GitHub!{theme['text']}
    """
    
    print(info)
    wait_for_enter()

def main():
    """Главная функция программы"""
    # Проверка зависимостей
    try:
        import pyperclip
        import qrcode
    except ImportError as e:
        print(f"{Fore.RED}Ошибка: Не установлена библиотека {e.name}")
        print(f"{Fore.YELLOW}Установите: pip install pyperclip qrcode[pil] colorama")
        input("\nНажмите Enter для выхода...")
        return
    
    # Показываем логотип
    show_logo()
    
    # Словарь функций
    functions = {
        '1': base64_tool,
        '2': hash_generator,
        '3': qr_generator,
        '4': url_tools,
        '5': password_generator,
        '6': text_analyzer,
        '7': json_formatter,
        '8': file_info,
        '9': process_monitor,
        '10': system_info,
        '11': internet_speed_test,
        '12': text_to_emoji,
        '13': color_palette_generator,
        '14': ascii_art_generator,
        '15': settings_menu,
        '99': about_program
    }
    
    # Главный цикл
    while True:
        choice = show_menu()
        
        if choice == '0':
            clear_screen()
            printc("Спасибо за использование EDGE UTILITY PRO!", "success")
            printc("До новых встреч! 👋", "accent")
            time.sleep(1)
            break
        
        elif choice in functions:
            try:
                if SETTINGS["log_operations"]:
                    with open("edge_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"{datetime.now()} - Выбрана функция {choice}\n")
                
                functions[choice]()
                
            except KeyboardInterrupt:
                clear_screen()
                printc("Операция прервана пользователем", "error")
                time.sleep(1)
                
            except Exception as e:
                printc(f"Ошибка: {e}", "error")
                wait_for_enter()
                
        else:
            printc("Неверный выбор!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        printc("\nПрограмма завершена пользователем", "error")
    except Exception as e:
        printc(f"\nКритическая ошибка: {e}", "error")
        input("Нажмите Enter для выхода...")