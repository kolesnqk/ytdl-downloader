#!/usr/bin/env python3
"""
Скрипт для показа скачанных файлов
"""

import os
import glob
from datetime import datetime

def show_downloads():
    """Показать скачанные файлы в текущей папке"""
    current_dir = os.getcwd()
    print(f"📁 Текущая папка: {current_dir}")
    print("=" * 60)
    
    # Ищем видео файлы
    video_extensions = ['*.mp4', '*.mkv', '*.webm', '*.avi', '*.mov', '*.flv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(glob.glob(ext))
        video_files.extend(glob.glob(ext.upper()))
    
    if video_files:
        print("🎥 Найденные видео файлы:")
        for i, file in enumerate(video_files, 1):
            file_path = os.path.join(current_dir, file)
            file_size = os.path.getsize(file_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Форматируем размер файла
            if file_size > 1024 * 1024 * 1024:  # GB
                size_str = f"{file_size / (1024 * 1024 * 1024):.1f} GB"
            elif file_size > 1024 * 1024:  # MB
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:  # KB
                size_str = f"{file_size / 1024:.1f} KB"
            
            print(f"{i:2d}. {file}")
            print(f"    📏 Размер: {size_str}")
            print(f"    📅 Дата: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    else:
        print("❌ Видео файлы не найдены")
    
    # Ищем временные файлы (.part)
    part_files = glob.glob("*.part")
    if part_files:
        print("⚠️  Найдены незавершенные скачивания:")
        for file in part_files:
            print(f"   - {file}")
        print()
    
    # Показываем общую информацию
    total_files = len(video_files)
    total_size = sum(os.path.getsize(f) for f in video_files)
    
    if total_size > 1024 * 1024 * 1024:
        total_size_str = f"{total_size / (1024 * 1024 * 1024):.1f} GB"
    elif total_size > 1024 * 1024:
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"📊 Всего файлов: {total_files}")
    print(f"📊 Общий размер: {total_size_str}")

if __name__ == "__main__":
    show_downloads()
