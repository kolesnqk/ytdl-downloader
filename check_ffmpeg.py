#!/usr/bin/env python3
"""
Проверка установки FFmpeg
"""

import subprocess
import sys

def check_ffmpeg():
    """Проверка установки FFmpeg"""
    print("🔍 Проверка установки FFmpeg...")
    print("=" * 40)
    
    try:
        # Проверяем FFmpeg
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Извлекаем версию из вывода
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg установлен: {version_line}")
            
            # Проверяем поддержку AAC кодека
            codec_result = subprocess.run(['ffmpeg', '-codecs'], 
                                        capture_output=True, text=True, timeout=10)
            
            if 'aac' in codec_result.stdout.lower():
                print("✅ Поддержка AAC кодека: есть")
            else:
                print("⚠️  Поддержка AAC кодека: не найдена")
            
            return True
        else:
            print("❌ FFmpeg не найден")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg не установлен")
        print("\n💡 Для установки FFmpeg:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   Linux: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Таймаут при проверке FFmpeg")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🎬 Проверка зависимостей для объединения видео...")
    print()
    
    ffmpeg_ok = check_ffmpeg()
    
    print("\n" + "=" * 40)
    
    if ffmpeg_ok:
        print("🎉 FFmpeg готов к работе!")
        print("✅ Video-only форматы будут корректно объединяться")
    else:
        print("❌ FFmpeg не готов")
        print("⚠️  Video-only форматы могут не объединяться")
    
    return ffmpeg_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
