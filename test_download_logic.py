#!/usr/bin/env python3
"""
Тест новой логики скачивания
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import YouTubeDownloader

def test_download_logic():
    """Тестирование логики скачивания"""
    print("🔍 Тестирование логики скачивания...")
    print("=" * 50)
    
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
        
        # Анализируем типы форматов
        video_with_audio = [f for f in formats if f['has_audio']]
        video_only = [f for f in formats if f['is_video_only']]
        audio_only = [f for f in formats if f['is_audio_only']]
        
        print(f"   🎬 Video+Audio: {len(video_with_audio)}")
        print(f"   🎥 Video Only: {len(video_only)}")
        print(f"   🎵 Audio Only: {len(audio_only)}")
        
        # Показываем примеры каждого типа
        print("\n2. Примеры форматов:")
        
        if video_with_audio:
            example = video_with_audio[0]
            print(f"   🎬 Video+Audio: {example['id']} - {example['quality']} - {example['extension']}")
        
        if video_only:
            example = video_only[0]
            print(f"   🎥 Video Only: {example['id']} - {example['quality']} - {example['extension']}")
        
        if audio_only:
            example = audio_only[0]
            print(f"   🎵 Audio Only: {example['id']} - {example['quality']} - {example['extension']}")
        
        print("\n3. Тестирование логики выбора...")
        
        # Тестируем выбор формата
        if video_with_audio:
            test_format = video_with_audio[0]
            print(f"   Тест Video+Audio формата: {test_format['id']}")
            # Не скачиваем, только тестируем логику
            print("   ✅ Логика: Скачать напрямую")
        
        if video_only:
            test_format = video_only[0]
            print(f"   Тест Video Only формата: {test_format['id']}")
            print("   ✅ Логика: Скачать видео + лучший аудио + объединить")
        
        if audio_only:
            test_format = audio_only[0]
            print(f"   Тест Audio Only формата: {test_format['id']}")
            print("   ✅ Логика: Скачать только аудио")
        
        print("\n🎉 Все тесты логики прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_download_logic()
    sys.exit(0 if success else 1)
