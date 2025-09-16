#!/usr/bin/env python3
"""
Скрипт для настройки Git репозитория
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Выполнение команды с обработкой ошибок"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            return True
        else:
            print(f"❌ {description} - ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False

def check_git():
    """Проверка установки Git"""
    print("🔍 Проверка установки Git...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git установлен: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git не найден")
            return False
    except FileNotFoundError:
        print("❌ Git не установлен")
        print("💡 Установите Git с https://git-scm.com/download/win")
        return False

def setup_git_repo():
    """Настройка Git репозитория"""
    print("🚀 Настройка Git репозитория...")
    print("=" * 50)
    
    # Проверяем Git
    if not check_git():
        return False
    
    # Инициализация репозитория
    if not run_command("git init", "Инициализация Git репозитория"):
        return False
    
    # Добавление файлов
    if not run_command("git add .", "Добавление файлов в Git"):
        return False
    
    # Первый коммит
    if not run_command('git commit -m "Initial commit: YouTube Video Downloader with PyQt5"', "Создание первого коммита"):
        return False
    
    print("\n✅ Git репозиторий настроен!")
    print("\n📋 Следующие шаги:")
    print("1. Создайте репозиторий на GitHub")
    print("2. Выполните команды:")
    print("   git remote add origin https://github.com/USERNAME/youtube-video-downloader.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n📖 Подробная инструкция в GITHUB_SETUP.md")
    
    return True

def main():
    print("🎬 Настройка YouTube Video Downloader для GitHub")
    print("=" * 60)
    
    # Проверяем, что мы в правильной папке
    if not os.path.exists("main.py"):
        print("❌ Ошибка: main.py не найден")
        print("💡 Запустите скрипт в папке с проектом")
        return False
    
    # Настраиваем Git
    if setup_git_repo():
        print("\n🎉 Настройка завершена!")
        return True
    else:
        print("\n❌ Настройка не удалась")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
