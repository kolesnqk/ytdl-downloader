#!/usr/bin/env python3
"""
Тест отображения размера файла
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import YouTubeDownloader

def test_size_display():
    """Тестирование отображения размера файла"""
    print("🔍 Тестирование отображения размера файла...")
    print("=" * 60)
    
    try:
        # Создаем экземпляр загрузчика
        downloader = YouTubeDownloader()
        print("✅ YouTubeDownloader создан")
        
        # Тестовая ссылка
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        print(f"📎 Тестовая ссылка: {test_url}")
        
        # Получаем форматы
        print("\n1. Получение форматов...")
        formats = downloader.get_available_formats(test_url)
        
        if not formats:
            print("❌ Не найдено форматов")
            return False
        
        print(f"✅ Найдено {len(formats)} форматов")
        
        # Тестируем получение размера для разных типов форматов
        print("\n2. Тестирование размеров файлов:")
        
        # Берем по одному примеру каждого типа
        video_with_audio = [f for f in formats if f['has_audio']]
        video_only = [f for f in formats if f['is_video_only']]
        audio_only = [f for f in formats if f['is_audio_only']]
        
        test_formats = []
        if video_with_audio:
            test_formats.append(("Video+Audio", video_with_audio[0]))
        if video_only:
            test_formats.append(("Video Only", video_only[0]))
        if audio_only:
            test_formats.append(("Audio Only", audio_only[0]))
        
        for format_type, fmt in test_formats:
            print(f"\n   {format_type}:")
            print(f"   ID: {fmt['id']}")
            print(f"   Качество: {fmt['quality']}")
            print(f"   Расширение: {fmt['extension']}")
            
            # Получаем размер
            size = downloader.get_format_size(test_url, fmt['id'])
            print(f"   📊 Размер: {size}")
        
        print("\n🎉 Тест размеров прошел успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_size_display()
    sys.exit(0 if success else 1)
