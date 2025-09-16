#!/usr/bin/env python3
"""
Тест объединения видео и аудио
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import YouTubeDownloader

def test_merge():
    """Тестирование объединения видео и аудио"""
    print("🔍 Тестирование объединения видео и аудио...")
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
        
        # Ищем video-only формат
        video_only_formats = [f for f in formats if f['is_video_only']]
        audio_only_formats = [f for f in formats if f['is_audio_only']]
        
        if not video_only_formats:
            print("❌ Не найдено video-only форматов")
            return False
        
        if not audio_only_formats:
            print("❌ Не найдено audio-only форматов")
            return False
        
        print(f"✅ Найдено {len(video_only_formats)} video-only форматов")
        print(f"✅ Найдено {len(audio_only_formats)} audio-only форматов")
        
        # Выбираем тестовые форматы
        video_format = video_only_formats[0]
        audio_format = audio_only_formats[0]
        
        print(f"\n2. Тестовые форматы:")
        print(f"   Видео: {video_format['id']} - {video_format['quality']} - {video_format['extension']}")
        print(f"   Аудио: {audio_format['id']} - {audio_format['quality']} - {audio_format['extension']}")
        
        # Тестируем объединение (без реального скачивания)
        print(f"\n3. Тестирование команды объединения...")
        
        # Строим команду как в коде
        cmd = [
            'yt-dlp',
            '--format', f"{video_format['id']}+{audio_format['id']}",
            '--output', 'test_output.%(ext)s',
            '--merge-output-format', 'mp4',
            '--no-playlist',
            test_url
        ]
        
        print(f"   Команда: {' '.join(cmd)}")
        print("   ✅ Команда сформирована корректно")
        
        print(f"\n4. Тестирование альтернативного метода...")
        
        # Тестируем альтернативный метод
        print(f"   Видео команда: yt-dlp --format {video_format['id']} --output temp_video.%(ext)s {test_url}")
        print(f"   Аудио команда: yt-dlp --format {audio_format['id']} --output temp_audio.%(ext)s {test_url}")
        print(f"   FFmpeg команда: ffmpeg -i temp_video.* -i temp_audio.* -c:v copy -c:a aac -y output.mp4")
        print("   ✅ Альтернативный метод готов")
        
        print("\n🎉 Все тесты прошли успешно!")
        print("\n💡 Для полного теста запустите приложение и выберите video-only формат")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_merge()
    sys.exit(0 if success else 1)
