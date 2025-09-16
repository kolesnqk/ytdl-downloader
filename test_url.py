#!/usr/bin/env python3
"""
Тест конкретной ссылки
"""

import subprocess
import sys
import json

def test_url(url):
    """Тестирование конкретной ссылки"""
    print(f"🔍 Тестирование ссылки: {url}")
    print("=" * 60)
    
    try:
        # Тест 1: Получение информации
        print("1. Получение информации о видео...")
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-download',
            '--socket-timeout', '30',
            '--retries', '3',
            '--fragment-retries', '3',
            url
        ]
        
        print(f"   Команда: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            video_info = json.loads(result.stdout)
            print(f"   ✅ Название: {video_info.get('title', 'Неизвестно')}")
            print(f"   ✅ Длительность: {video_info.get('duration', 0)} сек")
            print(f"   ✅ Загрузчик: {video_info.get('extractor', 'Неизвестно')}")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
        
        # Тест 2: Получение форматов
        print("\n2. Получение форматов...")
        cmd = [
            'yt-dlp',
            '--list-formats',
            '--socket-timeout', '30',
            '--retries', '3',
            '--fragment-retries', '3',
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            format_count = sum(1 for line in lines if line.strip() and line[0].isdigit())
            print(f"   ✅ Найдено форматов: {format_count}")
            
            # Показываем первые несколько форматов
            print("   Первые форматы:")
            for i, line in enumerate(lines[:10]):
                if line.strip() and line[0].isdigit():
                    print(f"     {line}")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
        
        print("\n🎉 Тест прошел успешно!")
        return True
        
    except subprocess.TimeoutExpired:
        print("   ❌ Таймаут при выполнении команды")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Тестовые ссылки
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
        ]
        
        print("Выберите тестовую ссылку:")
        for i, url in enumerate(test_urls, 1):
            print(f"{i}. {url}")
        
        try:
            choice = int(input("\nВведите номер (1-3): ")) - 1
            if 0 <= choice < len(test_urls):
                url = test_urls[choice]
            else:
                print("Неверный выбор!")
                return
        except (ValueError, KeyboardInterrupt):
            print("Отмена")
            return
    
    test_url(url)

if __name__ == "__main__":
    main()
