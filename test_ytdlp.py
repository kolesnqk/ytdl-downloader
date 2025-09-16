#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы yt-dlp
"""

import subprocess
import sys
import json

def test_ytdlp():
    """Тестирование yt-dlp"""
    print("🔍 Тестирование yt-dlp...")
    
    # Тестовая ссылка (короткое видео)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - короткое видео
    
    try:
        # Проверяем версию yt-dlp
        print("1. Проверка версии yt-dlp...")
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ Версия: {result.stdout.strip()}")
        else:
            print("   ❌ yt-dlp не работает")
            return False
        
        # Тестируем получение информации
        print("2. Тестирование получения информации о видео...")
        result = subprocess.run(['yt-dlp', '--dump-json', '--no-download', test_url], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            video_info = json.loads(result.stdout)
            print(f"   ✅ Название: {video_info.get('title', 'Неизвестно')}")
            print(f"   ✅ Длительность: {video_info.get('duration', 0)} сек")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
        
        # Тестируем получение форматов
        print("3. Тестирование получения форматов...")
        result = subprocess.run(['yt-dlp', '--list-formats', test_url], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            format_count = sum(1 for line in lines if line.strip() and line[0].isdigit())
            print(f"   ✅ Найдено форматов: {format_count}")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
        
        print("\n🎉 Все тесты прошли успешно!")
        return True
        
    except subprocess.TimeoutExpired:
        print("   ❌ Таймаут при выполнении команды")
        return False
    except FileNotFoundError:
        print("   ❌ yt-dlp не найден. Установите его: pip install yt-dlp")
        return False
    except Exception as e:
        print(f"   ❌ Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_ytdlp()
    sys.exit(0 if success else 1)
