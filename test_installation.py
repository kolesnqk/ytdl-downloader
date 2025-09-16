#!/usr/bin/env python3
"""
Скрипт для проверки установки зависимостей
"""

import sys
import subprocess

def check_package(package_name, import_name=None):
    """Проверка установки пакета"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} установлен")
        return True
    except ImportError:
        print(f"❌ {package_name} не установлен")
        return False

def check_ytdlp():
    """Проверка yt-dlp"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ yt-dlp установлен (версия: {result.stdout.strip()})")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ yt-dlp установлен как модуль (версия: {result.stdout.strip()})")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ yt-dlp не найден")
    return False

def check_ffmpeg():
    """Проверка FFmpeg"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg установлен: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg не найден")
    return False

def main():
    print("🔍 Проверка зависимостей...")
    print("=" * 50)
    
    # Проверяем Python версию
    python_version = sys.version_info
    print(f"Python версия: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 6):
        print("❌ Требуется Python 3.6 или выше")
        return False
    else:
        print("✅ Версия Python подходит")
    
    print("\n📦 Проверка пакетов:")
    
    # Проверяем PyQt5
    pyqt5_ok = check_package("PyQt5", "PyQt5.QtWidgets")
    
    # Проверяем yt-dlp
    ytdlp_ok = check_ytdlp()
    
    # Проверяем FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    print("\n" + "=" * 50)
    
    if pyqt5_ok and ytdlp_ok and ffmpeg_ok:
        print("🎉 Все зависимости установлены! Можно запускать приложение.")
        print("✅ yt-dlp и FFmpeg готовы к работе")
        print("✅ Video-only форматы будут корректно объединяться")
    elif pyqt5_ok and ytdlp_ok:
        print("⚠️  yt-dlp готов, но FFmpeg не найден")
        print("⚠️  Video-only форматы могут не объединяться")
    else:
        print("❌ Некоторые зависимости не установлены.")
        print("\nДля установки выполните:")
        print("  pip install -r requirements.txt")
        print("  И установите FFmpeg для объединения video-only форматов")
        return False
    
    print("\nДля запуска GUI приложения:")
    print("  python main.py")
    print("\nДля запуска консольной версии:")
    print("  python youtube_downloader.py")
    
    return True

if __name__ == "__main__":
    main()
