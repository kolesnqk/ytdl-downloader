#!/usr/bin/env python3
"""
YouTube Video Downloader using yt-dlp
Полный скрипт для скачивания видео с YouTube с выбором форматов
"""

import subprocess
import re
import sys
import os
from typing import List, Dict, Tuple, Optional


class YouTubeDownloader:
    """Класс для скачивания видео с YouTube используя yt-dlp"""
    
    def __init__(self):
        self.ytdlp_path = self._find_ytdlp()
        if not self.ytdlp_path:
            raise RuntimeError("yt-dlp не найден! Установите его: pip install yt-dlp")
    
    def _find_ytdlp(self) -> Optional[str]:
        """Поиск yt-dlp в системе"""
        try:
            # Проверяем, доступен ли yt-dlp в PATH
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return 'yt-dlp'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Проверяем локальную установку
        try:
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return f"{sys.executable} -m yt_dlp"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def get_video_info(self, url: str) -> Dict:
        """Получение информации о видео"""
        try:
            cmd = [self.ytdlp_path, '--dump-json', '--no-download', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка получения информации о видео: {result.stderr}")
            
            import json
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при получении информации о видео")
        except json.JSONDecodeError:
            raise RuntimeError("Ошибка парсинга информации о видео")
    
    def get_available_formats(self, url: str) -> List[Dict]:
        """Получение доступных форматов видео"""
        try:
            cmd = [self.ytdlp_path, '--list-formats', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка получения форматов: {result.stderr}")
            
            return self._parse_formats(result.stdout)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при получении форматов")
    
    def _parse_formats(self, formats_output: str) -> List[Dict]:
        """Парсинг вывода форматов yt-dlp"""
        formats = []
        lines = formats_output.split('\n')
        
        # Ищем строки с информацией о форматах
        for line in lines:
            if re.match(r'^\d+\s+', line):  # Строка начинается с ID формата
                parts = line.split()
                if len(parts) >= 4:
                    format_id = parts[0]
                    extension = parts[1]
                    resolution = parts[2] if len(parts) > 2 else "unknown"
                    note = " ".join(parts[3:]) if len(parts) > 3 else ""
                    
                    # Определяем тип формата
                    is_video_only = "video only" in note.lower()
                    is_audio_only = "audio only" in note.lower()
                    has_audio = not is_video_only and not is_audio_only
                    
                    # Извлекаем качество
                    quality = self._extract_quality(resolution, note)
                    
                    formats.append({
                        'id': format_id,
                        'extension': extension,
                        'resolution': resolution,
                        'quality': quality,
                        'note': note,
                        'is_video_only': is_video_only,
                        'is_audio_only': is_audio_only,
                        'has_audio': has_audio
                    })
        
        return formats
    
    def _extract_quality(self, resolution: str, note: str) -> str:
        """Извлечение качества из разрешения и заметки"""
        # Ищем разрешение в формате 1920x1080 или 1080p
        resolution_match = re.search(r'(\d+x\d+|\d+p)', resolution)
        if resolution_match:
            return resolution_match.group(1)
        
        # Ищем в заметке
        note_match = re.search(r'(\d+x\d+|\d+p)', note)
        if note_match:
            return note_match.group(1)
        
        return resolution
    
    def download_video(self, url: str, format_id: str, output_dir: str = ".") -> str:
        """Скачивание видео с выбранным форматом"""
        try:
            # Получаем информацию о формате
            formats = self.get_available_formats(url)
            selected_format = next((f for f in formats if f['id'] == format_id), None)
            
            if not selected_format:
                raise ValueError(f"Формат {format_id} не найден")
            
            # Строим команду для скачивания
            cmd = [
                self.ytdlp_path,
                '--format', format_id,
                '--output', os.path.join(output_dir, '%(title)s.%(ext)s'),
                '--no-playlist'
            ]
            
            # Если это video only, добавляем лучший аудио и объединяем
            if selected_format['is_video_only']:
                # Находим лучший аудио формат
                audio_formats = [f for f in formats if f['is_audio_only']]
                if audio_formats:
                    # Сортируем по качеству аудио (приоритет: mp3, m4a, webm)
                    audio_formats.sort(key=lambda x: (
                        x['extension'] == 'mp3',
                        x['extension'] == 'm4a', 
                        x['extension'] == 'webm',
                        x['quality']
                    ), reverse=True)
                    best_audio = audio_formats[0]
                    cmd.extend(['--format', f"{format_id}+{best_audio['id']}"])
                    cmd.extend(['--merge-output-format', 'mp4'])
                else:
                    print("Предупреждение: Не найден аудио формат для объединения")
            
            cmd.append(url)
            
            # Выполняем скачивание
            print(f"Скачивание видео в формате {format_id}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка скачивания: {result.stderr}")
            
            # Извлекаем имя файла из вывода
            output_match = re.search(r'\[download\] Destination: (.+)', result.stdout)
            if output_match:
                return output_match.group(1)
            else:
                return "Файл скачан успешно"
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при скачивании видео")
    
    def display_formats_menu(self, formats: List[Dict]) -> None:
        """Отображение меню доступных форматов"""
        print("\n" + "="*80)
        print("ДОСТУПНЫЕ ФОРМАТЫ ВИДЕО:")
        print("="*80)
        print(f"{'ID':<6} {'Качество':<12} {'Тип':<15} {'Расширение':<10} {'Описание'}")
        print("-"*80)
        
        for fmt in formats:
            format_type = "Video+Audio" if fmt['has_audio'] else ("Video Only" if fmt['is_video_only'] else "Audio Only")
            print(f"{fmt['id']:<6} {fmt['quality']:<12} {format_type:<15} {fmt['extension']:<10} {fmt['note']}")
        
        print("="*80)
    
    def get_user_choice(self, formats: List[Dict]) -> str:
        """Получение выбора пользователя"""
        while True:
            try:
                choice = input("\nВведите ID формата для скачивания (или 'q' для выхода): ").strip()
                
                if choice.lower() == 'q':
                    return None
                
                # Проверяем, существует ли выбранный формат
                if any(fmt['id'] == choice for fmt in formats):
                    return choice
                else:
                    print("❌ Неверный ID формата! Попробуйте снова.")
                    
            except KeyboardInterrupt:
                print("\n\nВыход...")
                return None
            except EOFError:
                print("\n\nВыход...")
                return None


def main():
    """Основная функция"""
    print("🎥 YouTube Video Downloader")
    print("=" * 50)
    
    try:
        # Создаем экземпляр загрузчика
        downloader = YouTubeDownloader()
        print("✅ yt-dlp найден и готов к работе")
        
        # Получаем URL от пользователя
        while True:
            url = input("\n📎 Введите URL видео YouTube: ").strip()
            if url:
                break
            print("❌ Пожалуйста, введите корректный URL")
        
        # Получаем информацию о видео
        print("\n🔍 Получение информации о видео...")
        try:
            video_info = downloader.get_video_info(url)
            print(f"✅ Найдено видео: {video_info.get('title', 'Неизвестно')}")
        except Exception as e:
            print(f"❌ Ошибка получения информации: {e}")
            return
        
        # Получаем доступные форматы
        print("📋 Получение доступных форматов...")
        try:
            formats = downloader.get_available_formats(url)
            if not formats:
                print("❌ Не найдено доступных форматов")
                return
        except Exception as e:
            print(f"❌ Ошибка получения форматов: {e}")
            return
        
        # Отображаем меню форматов
        downloader.display_formats_menu(formats)
        
        # Получаем выбор пользователя
        choice = downloader.get_user_choice(formats)
        if not choice:
            print("👋 До свидания!")
            return
        
        # Скачиваем видео
        print(f"\n⬇️  Начинаем скачивание...")
        try:
            output_file = downloader.download_video(url, choice)
            print(f"✅ Видео успешно скачано: {output_file}")
        except Exception as e:
            print(f"❌ Ошибка скачивания: {e}")
            return
        
    except RuntimeError as e:
        print(f"❌ {e}")
        print("\n💡 Для установки yt-dlp выполните:")
        print("   pip install yt-dlp")
    except KeyboardInterrupt:
        print("\n\n👋 Выход...")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
