#!/usr/bin/env python3
"""
Тест ручного объединения
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import YouTubeDownloader

def test_manual_merge():
    """Тестирование ручного объединения"""
    print("🔍 Тестирование ручного объединения...")
    print("=" * 60)
    
    try:
        # Создаем экземпляр загрузчика
        downloader = YouTubeDownloader()
        print("✅ YouTubeDownloader создан")
        
        # Тестовая ссылка (короткое видео)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        print(f"📎 Тестовая ссылка: {test_url}")
        
        # Получаем форматы
        print("\n1. Получение форматов...")
        formats = downloader.get_available_formats(test_url)
        
        if not formats:
            print("❌ Не найдено форматов")
            return False
        
        print(f"✅ Найдено {len(formats)} форматов")
        
        # Ищем video-only и audio-only форматы
        video_only_formats = [f for f in formats if f['is_video_only']]
        audio_only_formats = [f for f in formats if f['is_audio_only']]
        
        if not video_only_formats or not audio_only_formats:
            print("❌ Не найдено нужных форматов")
            print(f"   Video-only: {len(video_only_formats)}")
            print(f"   Audio-only: {len(audio_only_formats)}")
            return False
        
        # Выбираем форматы
        video_format = video_only_formats[0]
        audio_format = audio_only_formats[0]
        
        print(f"\n2. Выбранные форматы:")
        print(f"   Видео: {video_format['id']} - {video_format['quality']} - {video_format['extension']}")
        print(f"   Аудио: {audio_format['id']} - {audio_format['quality']} - {audio_format['extension']}")
        
        # Тестируем ручное объединение
        print(f"\n3. Тестирование ручного объединения...")
        
        # Создаем тестовую папку
        test_dir = "test_merge_output"
        os.makedirs(test_dir, exist_ok=True)
        
        try:
            result = downloader._download_and_merge_manually(
                test_url, 
                video_format['id'], 
                audio_format['id'], 
                test_dir
            )
            
            if result['success']:
                print(f"✅ Объединение успешно!")
                print(f"   Файл: {result['final_file']}")
                print(f"   Сообщение: {result['message']}")
                
                # Проверяем размер файла
                if os.path.exists(result['final_file']):
                    file_size = os.path.getsize(result['final_file'])
                    print(f"   Размер: {file_size} байт")
                
                return True
            else:
                print(f"❌ Ошибка объединения: {result['message']}")
                return False
                
        finally:
            # Очищаем тестовую папку
            import shutil
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)
                print(f"   Тестовая папка {test_dir} удалена")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_manual_merge()
    sys.exit(0 if success else 1)
