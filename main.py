import sys
import os
import subprocess
import re
import json
import glob
from typing import List, Dict, Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTextEdit, QComboBox, QProgressBar,
                             QGroupBox, QGridLayout, QScrollArea, QFrame,
                             QFileDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap


class YouTubeDownloader:
    """Класс для скачивания видео с YouTube используя yt-dlp"""
    
    def __init__(self):
        self.ytdlp_path = self._find_ytdlp()
        if not self.ytdlp_path:
            raise RuntimeError("yt-dlp не найден! Установите его: pip install yt-dlp")
        
        # Проверяем FFmpeg
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            print("⚠️  Предупреждение: FFmpeg не найден. Video-only форматы могут не объединяться.")
    
    def _find_ytdlp(self) -> Optional[str]:
        """Поиск yt-dlp в системе"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return 'yt-dlp'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        try:
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return f"{sys.executable} -m yt_dlp"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def _check_ffmpeg(self) -> bool:
        """Проверка наличия FFmpeg"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_video_info(self, url: str) -> Dict:
        """Получение информации о видео"""
        try:
            # Разбиваем команду на части для лучшей обработки
            if isinstance(self.ytdlp_path, str) and ' ' in self.ytdlp_path:
                cmd = self.ytdlp_path.split() + [
                    '--dump-json', 
                    '--no-download',
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            else:
                cmd = [
                    self.ytdlp_path, 
                    '--dump-json', 
                    '--no-download',
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if "Video unavailable" in error_msg:
                    raise RuntimeError("Видео недоступно или приватное")
                elif "Private video" in error_msg:
                    raise RuntimeError("Видео приватное")
                elif "Video unavailable" in error_msg:
                    raise RuntimeError("Видео недоступно")
                elif "HTTP Error 403" in error_msg:
                    raise RuntimeError("Доступ запрещен (403). Попробуйте другую ссылку")
                elif "HTTP Error 404" in error_msg:
                    raise RuntimeError("Видео не найдено (404)")
                else:
                    raise RuntimeError(f"Ошибка получения информации: {error_msg}")
            
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при получении информации о видео (60 сек). Проверьте интернет-соединение")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Ошибка парсинга JSON: {e}")
        except FileNotFoundError:
            raise RuntimeError("yt-dlp не найден в системе")
    
    def get_format_size(self, url: str, format_id: str) -> str:
        """Получение размера файла для конкретного формата"""
        try:
            # Получаем детальную информацию о формате
            if isinstance(self.ytdlp_path, str) and ' ' in self.ytdlp_path:
                cmd = self.ytdlp_path.split() + [
                    '--dump-json',
                    '--no-download',
                    '--format', format_id,
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            else:
                cmd = [
                    self.ytdlp_path,
                    '--dump-json',
                    '--no-download',
                    '--format', format_id,
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return "Размер неизвестен"
            
            data = json.loads(result.stdout)
            
            # Ищем информацию о размере в форматах
            if 'formats' in data:
                for fmt in data['formats']:
                    if fmt.get('format_id') == format_id:
                        filesize = fmt.get('filesize')
                        if filesize:
                            return self._format_file_size(filesize)
            
            # Если не нашли в форматах, ищем общий размер
            if 'filesize' in data and data['filesize']:
                return self._format_file_size(data['filesize'])
            
            return "Размер неизвестен"
            
        except Exception:
            return "Размер неизвестен"
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Форматирование размера файла"""
        if size_bytes is None:
            return "Размер неизвестен"
        
        if size_bytes >= 1024 * 1024 * 1024:  # GB
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
        elif size_bytes >= 1024 * 1024:  # MB
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        elif size_bytes >= 1024:  # KB
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes} байт"
    
    def get_available_formats(self, url: str) -> List[Dict]:
        """Получение доступных форматов видео"""
        try:
            # Разбиваем команду на части для лучшей обработки
            if isinstance(self.ytdlp_path, str) and ' ' in self.ytdlp_path:
                cmd = self.ytdlp_path.split() + [
                    '--list-formats',
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            else:
                cmd = [
                    self.ytdlp_path, 
                    '--list-formats',
                    '--socket-timeout', '30',
                    '--retries', '3',
                    '--fragment-retries', '3',
                    url
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                raise RuntimeError(f"Ошибка получения форматов: {error_msg}")
            
            return self._parse_formats(result.stdout)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при получении форматов (60 сек). Проверьте интернет-соединение")
        except FileNotFoundError:
            raise RuntimeError("yt-dlp не найден в системе")
    
    def _parse_formats(self, formats_output: str) -> List[Dict]:
        """Парсинг вывода форматов yt-dlp"""
        formats = []
        lines = formats_output.split('\n')
        
        for line in lines:
            if re.match(r'^\d+\s+', line):
                parts = line.split()
                if len(parts) >= 4:
                    format_id = parts[0]
                    extension = parts[1]
                    resolution = parts[2] if len(parts) > 2 else "unknown"
                    note = " ".join(parts[3:]) if len(parts) > 3 else ""
                    
                    is_video_only = "video only" in note.lower()
                    is_audio_only = "audio only" in note.lower()
                    has_audio = not is_video_only and not is_audio_only
                    
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
        resolution_match = re.search(r'(\d+x\d+|\d+p)', resolution)
        if resolution_match:
            return resolution_match.group(1)
        
        note_match = re.search(r'(\d+x\d+|\d+p)', note)
        if note_match:
            return note_match.group(1)
        
        return resolution
    
    def download_video(self, url: str, format_id: str, output_dir: str = ".") -> Dict:
        """Скачивание видео с выбранным форматом"""
        try:
            formats = self.get_available_formats(url)
            selected_format = next((f for f in formats if f['id'] == format_id), None)
            
            if not selected_format:
                raise ValueError(f"Формат {format_id} не найден")
            
            result = {
                'success': False,
                'video_file': None,
                'audio_file': None,
                'final_file': None,
                'message': '',
                'format_type': 'unknown'
            }
            
            if selected_format['is_video_only']:
                # Скачиваем video only + лучший аудио отдельно, затем объединяем
                result['format_type'] = 'video_only'
                return self._download_video_with_audio(url, format_id, output_dir, formats)
                
            elif selected_format['is_audio_only']:
                # Скачиваем только аудио
                result['format_type'] = 'audio_only'
                return self._download_audio_only(url, format_id, output_dir)
                
            else:
                # Скачиваем видео с аудио (обычный формат)
                result['format_type'] = 'video_with_audio'
                return self._download_video_with_audio_direct(url, format_id, output_dir)
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Таймаут при скачивании видео")
    
    def _download_video_with_audio(self, url: str, video_format_id: str, output_dir: str, formats: List[Dict]) -> Dict:
        """Скачивание video only + аудио с последующим объединением"""
        result = {
            'success': False,
            'video_file': None,
            'audio_file': None,
            'final_file': None,
            'message': '',
            'format_type': 'video_only'
        }
        
        try:
            # Находим лучший аудио формат
            audio_formats = [f for f in formats if f['is_audio_only']]
            if not audio_formats:
                raise RuntimeError("Не найден аудио формат для объединения")
            
            # Сортируем аудио форматы по приоритету
            audio_formats.sort(key=lambda x: (
                x['extension'] == 'mp3',
                x['extension'] == 'm4a', 
                x['extension'] == 'webm',
                x['quality']
            ), reverse=True)
            
            best_audio = audio_formats[0]
            
            # Сразу используем ручное объединение, так как yt-dlp с + не всегда работает корректно
            print("Используем ручное объединение для гарантированного результата...")
            return self._download_and_merge_manually(url, video_format_id, best_audio['id'], output_dir)
                
        except Exception as e:
            result['message'] = f"Ошибка при скачивании video+audio: {e}"
            
        return result
    
    def _download_and_merge_manually(self, url: str, video_format_id: str, audio_format_id: str, output_dir: str) -> Dict:
        """Альтернативный метод: скачивание и ручное объединение"""
        result = {
            'success': False,
            'video_file': None,
            'audio_file': None,
            'final_file': None,
            'message': '',
            'format_type': 'video_only'
        }
        
        try:
            # Проверяем наличие FFmpeg
            if not self.ffmpeg_available:
                raise RuntimeError("FFmpeg не найден! Установите FFmpeg для объединения video-only форматов.")
            
            # Получаем название видео для финального файла
            video_info = self.get_video_info(url)
            title = video_info.get('title', 'video')
            # Очищаем название от недопустимых символов
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            final_file = os.path.join(output_dir, f"{title}.mp4")
            
            # Генерируем уникальные имена для временных файлов
            import time
            timestamp = str(int(time.time()))
            temp_video = os.path.join(output_dir, f"temp_video_{timestamp}.%(ext)s")
            temp_audio = os.path.join(output_dir, f"temp_audio_{timestamp}.%(ext)s")
            
            # Скачиваем видео отдельно
            video_cmd = [
                self.ytdlp_path,
                '--format', video_format_id,
                '--output', temp_video,
                '--no-playlist'
            ]
            
            print(f"Скачивание видео: {' '.join(video_cmd + [url])}")
            video_result = subprocess.run(video_cmd + [url], capture_output=True, text=True, timeout=300)
            
            if video_result.returncode != 0:
                raise RuntimeError(f"Ошибка скачивания видео: {video_result.stderr}")
            
            # Скачиваем аудио отдельно
            audio_cmd = [
                self.ytdlp_path,
                '--format', audio_format_id,
                '--output', temp_audio,
                '--no-playlist'
            ]
            
            print(f"Скачивание аудио: {' '.join(audio_cmd + [url])}")
            audio_result = subprocess.run(audio_cmd + [url], capture_output=True, text=True, timeout=300)
            
            if audio_result.returncode != 0:
                raise RuntimeError(f"Ошибка скачивания аудио: {audio_result.stderr}")
            
            # Ищем скачанные файлы
            video_pattern = os.path.join(output_dir, f"temp_video_{timestamp}.*")
            audio_pattern = os.path.join(output_dir, f"temp_audio_{timestamp}.*")
            
            video_files = glob.glob(video_pattern)
            audio_files = glob.glob(audio_pattern)
            
            if not video_files or not audio_files:
                print(f"Ищем файлы по паттернам:")
                print(f"  Видео: {video_pattern}")
                print(f"  Аудио: {audio_pattern}")
                print(f"  Найдено видео: {video_files}")
                print(f"  Найдено аудио: {audio_files}")
                raise RuntimeError("Не удалось найти скачанные файлы")
            
            video_file = video_files[0]
            audio_file = audio_files[0]
            
            print(f"Найдены файлы:")
            print(f"  Видео: {video_file}")
            print(f"  Аудио: {audio_file}")
            
            # Объединяем с помощью ffmpeg
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-y',  # Перезаписывать файл если существует
                final_file
            ]
            
            print(f"Объединение файлов: {' '.join(ffmpeg_cmd)}")
            merge_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)
            
            if merge_result.returncode != 0:
                print(f"Ошибка FFmpeg stderr: {merge_result.stderr}")
                print(f"Ошибка FFmpeg stdout: {merge_result.stdout}")
                raise RuntimeError(f"Ошибка объединения: {merge_result.stderr}")
            
            # Проверяем, что финальный файл создан
            if not os.path.exists(final_file):
                raise RuntimeError("Финальный файл не был создан")
            
            # Удаляем временные файлы
            try:
                os.remove(video_file)
                os.remove(audio_file)
                print("Временные файлы удалены")
            except Exception as e:
                print(f"Предупреждение: не удалось удалить временные файлы: {e}")
            
            result['final_file'] = final_file
            result['success'] = True
            result['message'] = f"Видео и аудио успешно скачаны и объединены в: {os.path.basename(final_file)}"
            
        except Exception as e:
            result['message'] = f"Ошибка при ручном объединении: {e}"
            print(f"Ошибка: {e}")
            
        return result
    
    def _download_audio_only(self, url: str, audio_format_id: str, output_dir: str) -> Dict:
        """Скачивание только аудио"""
        result = {
            'success': False,
            'video_file': None,
            'audio_file': None,
            'final_file': None,
            'message': '',
            'format_type': 'audio_only'
        }
        
        try:
            cmd = [
                self.ytdlp_path,
                '--format', audio_format_id,
                '--output', os.path.join(output_dir, '%(title)s.%(ext)s'),
                '--no-playlist'
            ]
            
            result_cmd = subprocess.run(cmd + [url], capture_output=True, text=True, timeout=300)
            
            if result_cmd.returncode != 0:
                raise RuntimeError(f"Ошибка скачивания: {result_cmd.stderr}")
            
            # Ищем скачанный файл
            output_match = re.search(r'\[download\] Destination: (.+)', result_cmd.stdout)
            if output_match:
                result['final_file'] = output_match.group(1)
                result['success'] = True
                result['message'] = f"Аудио успешно скачано: {os.path.basename(result['final_file'])}"
            else:
                raise RuntimeError("Не удалось определить путь к скачанному файлу")
                
        except Exception as e:
            result['message'] = f"Ошибка при скачивании аудио: {e}"
            
        return result
    
    def _download_video_with_audio_direct(self, url: str, format_id: str, output_dir: str) -> Dict:
        """Скачивание видео с аудио напрямую"""
        result = {
            'success': False,
            'video_file': None,
            'audio_file': None,
            'final_file': None,
            'message': '',
            'format_type': 'video_with_audio'
        }
        
        try:
            cmd = [
                self.ytdlp_path,
                '--format', format_id,
                '--output', os.path.join(output_dir, '%(title)s.%(ext)s'),
                '--no-playlist'
            ]
            
            result_cmd = subprocess.run(cmd + [url], capture_output=True, text=True, timeout=300)
            
            if result_cmd.returncode != 0:
                raise RuntimeError(f"Ошибка скачивания: {result_cmd.stderr}")
            
            # Ищем скачанный файл
            output_match = re.search(r'\[download\] Destination: (.+)', result_cmd.stdout)
            if output_match:
                result['final_file'] = output_match.group(1)
                result['success'] = True
                result['message'] = f"Видео с аудио успешно скачано: {os.path.basename(result['final_file'])}"
            else:
                raise RuntimeError("Не удалось определить путь к скачанному файлу")
                
        except Exception as e:
            result['message'] = f"Ошибка при скачивании: {e}"
            
        return result


class InfoThread(QThread):
    """Поток для получения информации о видео"""
    progress = pyqtSignal(str)
    video_info_ready = pyqtSignal(dict)
    formats_ready = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, downloader, url):
        super().__init__()
        self.downloader = downloader
        self.url = url
    
    def run(self):
        try:
            self.progress.emit("Получение информации о видео...")
            video_info = self.downloader.get_video_info(self.url)
            self.video_info_ready.emit(video_info)
            
            self.progress.emit("Получение доступных форматов...")
            formats = self.downloader.get_available_formats(self.url)
            self.formats_ready.emit(formats)
            
        except Exception as e:
            self.error.emit(str(e))


class FormatSizeThread(QThread):
    """Поток для получения размера файла"""
    size_ready = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, downloader, url, format_id, selected_format):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.format_id = format_id
        self.selected_format = selected_format
    
    def run(self):
        try:
            # Получаем размер файла
            size = self.downloader.get_format_size(self.url, self.format_id)
            
            # Определяем тип формата
            if self.selected_format['is_video_only']:
                format_type = 'video_only'
            elif self.selected_format['is_audio_only']:
                format_type = 'audio_only'
            else:
                format_type = 'video_with_audio'
            
            self.size_ready.emit({
                'size': size,
                'format_type': format_type
            })
            
        except Exception as e:
            self.error.emit(str(e))


class DownloadThread(QThread):
    """Поток для скачивания видео"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)  # Теперь передаем словарь с результатом
    error = pyqtSignal(str)
    
    def __init__(self, downloader, url, format_id, output_dir="."):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.format_id = format_id
        self.output_dir = output_dir
    
    def run(self):
        try:
            # Получаем информацию о выбранном формате
            formats = self.downloader.get_available_formats(self.url)
            selected_format = next((f for f in formats if f['id'] == self.format_id), None)
            
            if selected_format:
                if selected_format['is_video_only']:
                    self.progress.emit("Скачивание видео и аудио с последующим объединением...")
                elif selected_format['is_audio_only']:
                    self.progress.emit("Скачивание аудио...")
                else:
                    self.progress.emit("Скачивание видео с аудио...")
            else:
                self.progress.emit("Начинаем скачивание...")
            
            result = self.downloader.download_video(self.url, self.format_id, self.output_dir)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class LinkInputWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.downloader = None
        self.video_info = None
        self.formats = []
        self.download_thread = None
        self.info_thread = None
        self.size_thread = None
        self.download_dir = os.getcwd()  # Текущая папка по умолчанию
        self.init_ui()
        
    def init_ui(self):
        # Настройка основного окна
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(300, 300, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Заголовок
        title_label = QLabel("🎥 YouTube Video Downloader")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Группа для ввода URL
        url_group = QGroupBox("Введите ссылку на видео")
        url_layout = QVBoxLayout()
        url_group.setLayout(url_layout)
        
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.link_input.setFont(QFont("Arial", 11))
        url_layout.addWidget(self.link_input)
        
        # Кнопки для URL
        url_button_layout = QHBoxLayout()
        
        self.get_info_button = QPushButton("Получить информацию")
        self.get_info_button.setFont(QFont("Arial", 11))
        self.get_info_button.setMinimumHeight(35)
        self.get_info_button.clicked.connect(self.on_get_info_clicked)
        
        self.clear_url_button = QPushButton("Очистить")
        self.clear_url_button.setFont(QFont("Arial", 11))
        self.clear_url_button.setMinimumHeight(35)
        self.clear_url_button.clicked.connect(self.on_clear_url_clicked)
        
        url_button_layout.addWidget(self.clear_url_button)
        url_button_layout.addWidget(self.get_info_button)
        url_layout.addLayout(url_button_layout)
        
        main_layout.addWidget(url_group)
        
        # Группа для выбора папки скачивания
        download_group = QGroupBox("Папка для скачивания")
        download_layout = QHBoxLayout()
        download_group.setLayout(download_layout)
        
        self.download_path_label = QLabel(f"📁 {self.download_dir}")
        self.download_path_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; border-radius: 3px; }")
        self.download_path_label.setWordWrap(True)
        download_layout.addWidget(self.download_path_label)
        
        self.browse_button = QPushButton("Выбрать папку")
        self.browse_button.setFont(QFont("Arial", 10))
        self.browse_button.setMinimumHeight(30)
        self.browse_button.clicked.connect(self.on_browse_clicked)
        download_layout.addWidget(self.browse_button)
        
        main_layout.addWidget(download_group)
        
        # Информация о видео
        self.video_info_label = QLabel("")
        self.video_info_label.setWordWrap(True)
        self.video_info_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }")
        main_layout.addWidget(self.video_info_label)
        
        # Группа для выбора формата
        self.format_group = QGroupBox("Выберите формат для скачивания")
        self.format_group.setVisible(False)
        format_layout = QVBoxLayout()
        self.format_group.setLayout(format_layout)
        
        # ComboBox для выбора формата
        self.format_combo = QComboBox()
        self.format_combo.setFont(QFont("Arial", 10))
        self.format_combo.currentIndexChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.format_combo)
        
        # Label для отображения размера файла
        self.size_label = QLabel("")
        self.size_label.setStyleSheet("QLabel { background-color: #e8f4f8; padding: 5px; border-radius: 3px; font-weight: bold; }")
        self.size_label.setAlignment(Qt.AlignCenter)
        format_layout.addWidget(self.size_label)
        
        # Кнопки для скачивания
        download_button_layout = QHBoxLayout()
        
        self.download_button = QPushButton("Скачать")
        self.download_button.setFont(QFont("Arial", 11))
        self.download_button.setMinimumHeight(35)
        self.download_button.clicked.connect(self.on_download_clicked)
        self.download_button.setEnabled(False)
        
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setFont(QFont("Arial", 11))
        self.cancel_button.setMinimumHeight(35)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        
        download_button_layout.addWidget(self.cancel_button)
        download_button_layout.addWidget(self.download_button)
        format_layout.addLayout(download_button_layout)
        
        main_layout.addWidget(self.format_group)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)
        
        # Обработка нажатия Enter в поле ввода
        self.link_input.returnPressed.connect(self.on_get_info_clicked)
        
        # Фокус на поле ввода
        self.link_input.setFocus()
        
        # Инициализация загрузчика
        try:
            self.downloader = YouTubeDownloader()
            if self.downloader.ffmpeg_available:
                self.status_label.setText("✅ yt-dlp и FFmpeg готовы к работе")
            else:
                self.status_label.setText("⚠️ yt-dlp готов, но FFmpeg не найден. Video-only форматы могут не объединяться.")
        except RuntimeError as e:
            self.status_label.setText(f"❌ {e}")
            self.get_info_button.setEnabled(False)
        
    def on_get_info_clicked(self):
        """Обработчик нажатия кнопки 'Получить информацию'"""
        url = self.link_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите ссылку!")
            return
        
        if not self.downloader:
            QMessageBox.critical(self, "Ошибка", "yt-dlp не инициализирован!")
            return
        
        # Останавливаем предыдущий поток, если он запущен
        if self.info_thread and self.info_thread.isRunning():
            self.info_thread.terminate()
            self.info_thread.wait()
        
        # Создаем новый поток для получения информации
        self.info_thread = InfoThread(self.downloader, url)
        self.info_thread.progress.connect(self.on_info_progress)
        self.info_thread.video_info_ready.connect(self.on_video_info_ready)
        self.info_thread.formats_ready.connect(self.on_formats_ready)
        self.info_thread.error.connect(self.on_info_error)
        
        # Показываем прогресс
        self.status_label.setText("🔍 Получение информации о видео...")
        self.get_info_button.setEnabled(False)
        self.format_group.setVisible(False)
        
        # Запускаем поток
        self.info_thread.start()
    
    def on_info_progress(self, message):
        """Обработчик прогресса получения информации"""
        self.status_label.setText(f"🔍 {message}")
    
    def on_video_info_ready(self, video_info):
        """Обработчик получения информации о видео"""
        self.video_info = video_info
        title = video_info.get('title', 'Неизвестно')
        duration = video_info.get('duration', 0)
        
        # Форматируем длительность
        if duration:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            if hours:
                duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                duration_str = f"{minutes:02d}:{seconds:02d}"
        else:
            duration_str = "Неизвестно"
        
        # Показываем информацию о видео
        self.video_info_label.setText(
            f"📺 <b>Название:</b> {title}<br>"
            f"⏱️ <b>Длительность:</b> {duration_str}<br>"
            f"🔗 <b>URL:</b> {self.link_input.text().strip()}"
        )
    
    def on_formats_ready(self, formats):
        """Обработчик получения форматов"""
        self.formats = formats
        
        if not formats:
            QMessageBox.warning(self, "Предупреждение", "Не найдено доступных форматов!")
            self.status_label.setText("❌ Не найдено доступных форматов")
            self.get_info_button.setEnabled(True)
            return
        
        # Заполняем ComboBox форматами
        self.format_combo.clear()
        for fmt in formats:
            if fmt['has_audio']:
                format_type = "🎬 Video+Audio"
                icon = "🎬"
            elif fmt['is_video_only']:
                if self.downloader.ffmpeg_available:
                    format_type = "🎥 Video Only (будет объединено с аудио)"
                    icon = "🎥"
                else:
                    format_type = "🎥 Video Only (⚠️ FFmpeg не найден!)"
                    icon = "⚠️"
            else:  # audio_only
                format_type = "🎵 Audio Only"
                icon = "🎵"
            
            display_text = f"{icon} {fmt['id']} - {fmt['quality']} ({format_type}) - {fmt['extension']}"
            self.format_combo.addItem(display_text, fmt['id'])
        
        # Сохраняем форматы для использования в обработчике
        self.formats = formats
        
        # Показываем группу выбора формата
        self.format_group.setVisible(True)
        self.download_button.setEnabled(True)
        self.status_label.setText("✅ Выберите формат для скачивания")
        self.get_info_button.setEnabled(True)
    
    def on_info_error(self, error):
        """Обработчик ошибки получения информации"""
        QMessageBox.critical(self, "Ошибка", f"Ошибка получения информации: {error}")
        self.status_label.setText(f"❌ Ошибка: {error}")
        self.get_info_button.setEnabled(True)
    
    def on_format_changed(self, index):
        """Обработчик изменения выбора формата"""
        if index == -1 or not hasattr(self, 'formats') or not self.formats:
            self.size_label.setText("")
            return
        
        try:
            format_id = self.format_combo.currentData()
            if not format_id:
                self.size_label.setText("")
                return
            
            # Находим выбранный формат
            selected_format = next((f for f in self.formats if f['id'] == format_id), None)
            if not selected_format:
                self.size_label.setText("")
                return
            
            # Показываем загрузку размера
            self.size_label.setText("📊 Получение размера файла...")
            
            # Получаем размер файла в отдельном потоке
            self.size_thread = FormatSizeThread(self.downloader, self.link_input.text().strip(), format_id, selected_format)
            self.size_thread.size_ready.connect(self.on_size_ready)
            self.size_thread.error.connect(self.on_size_error)
            self.size_thread.start()
            
        except Exception as e:
            self.size_label.setText(f"❌ Ошибка: {e}")
    
    def on_size_ready(self, size_info):
        """Обработчик получения размера файла"""
        format_type = size_info['format_type']
        size = size_info['size']
        
        if format_type == 'video_only':
            self.size_label.setText(f"📊 Размер: {size} (видео + аудио + объединение)")
        elif format_type == 'audio_only':
            self.size_label.setText(f"📊 Размер: {size} (только аудио)")
        else:  # video_with_audio
            self.size_label.setText(f"📊 Размер: {size} (видео с аудио)")
    
    def on_size_error(self, error):
        """Обработчик ошибки получения размера"""
        self.size_label.setText(f"❌ Размер неизвестен: {error}")
    
    def on_browse_clicked(self):
        """Обработчик нажатия кнопки 'Выбрать папку'"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку для скачивания", 
            self.download_dir
        )
        
        if folder:
            self.download_dir = folder
            self.download_path_label.setText(f"📁 {self.download_dir}")
            self.status_label.setText(f"✅ Папка для скачивания: {self.download_dir}")
    
    def on_download_clicked(self):
        """Обработчик нажатия кнопки 'Скачать'"""
        if not self.formats or self.format_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Предупреждение", "Выберите формат для скачивания!")
            return
        
        format_id = self.format_combo.currentData()
        url = self.link_input.text().strip()
        
        # Проверяем, является ли выбранный формат video-only
        selected_format = next((f for f in self.formats if f['id'] == format_id), None)
        if selected_format and selected_format['is_video_only'] and not self.downloader.ffmpeg_available:
            reply = QMessageBox.question(
                self, 
                "Предупреждение", 
                "Выбран video-only формат, но FFmpeg не найден!\n\n"
                "Без FFmpeg видео и аудио не будут объединены в один файл.\n"
                "Установите FFmpeg для корректной работы.\n\n"
                "Продолжить скачивание?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # Создаем поток для скачивания с выбранной папкой
        self.download_thread = DownloadThread(self.downloader, url, format_id, self.download_dir)
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        
        # Показываем прогресс
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Неопределенный прогресс
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.status_label.setText(f"⬇️ Скачивание в папку: {self.download_dir}")
        
        # Запускаем скачивание
        self.download_thread.start()
    
    def on_cancel_clicked(self):
        """Обработчик нажатия кнопки 'Отмена'"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        
        self.progress_bar.setVisible(False)
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.status_label.setText("❌ Скачивание отменено")
    
    def on_download_progress(self, message):
        """Обработчик прогресса скачивания"""
        self.status_label.setText(f"⬇️ {message}")
    
    def on_download_finished(self, result):
        """Обработчик завершения скачивания"""
        self.progress_bar.setVisible(False)
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if result['success']:
            self.status_label.setText("✅ Скачивание завершено!")
            
            # Формируем сообщение в зависимости от типа скачивания
            if result['format_type'] == 'video_only':
                message = f"🎥 Видео и аудио успешно скачаны и объединены!\n\n"
            elif result['format_type'] == 'audio_only':
                message = f"🎵 Аудио успешно скачано!\n\n"
            else:  # video_with_audio
                message = f"🎬 Видео с аудио успешно скачано!\n\n"
            
            # Добавляем информацию о файле
            if result['final_file']:
                full_path = os.path.abspath(result['final_file'])
                message += f"📁 Папка: {self.download_dir}\n"
                message += f"📄 Файл: {os.path.basename(result['final_file'])}\n"
                message += f"🔗 Полный путь: {full_path}\n\n"
                message += f"💬 {result['message']}"
            
            QMessageBox.information(self, "Успех", message)
        else:
            self.status_label.setText("❌ Ошибка скачивания")
            QMessageBox.critical(self, "Ошибка", f"Ошибка скачивания:\n{result['message']}")
    
    def on_download_error(self, error):
        """Обработчик ошибки скачивания"""
        self.progress_bar.setVisible(False)
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.status_label.setText(f"❌ Ошибка скачивания: {error}")
        
        QMessageBox.critical(self, "Ошибка", f"Ошибка скачивания:\n{error}")
    
    def on_clear_url_clicked(self):
        """Обработчик нажатия кнопки 'Очистить'"""
        # Останавливаем все потоки
        if self.info_thread and self.info_thread.isRunning():
            self.info_thread.terminate()
            self.info_thread.wait()
        
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        
        if self.size_thread and self.size_thread.isRunning():
            self.size_thread.terminate()
            self.size_thread.wait()
        
        self.link_input.clear()
        self.video_info_label.setText("")
        self.format_group.setVisible(False)
        self.progress_bar.setVisible(False)
        self.size_label.setText("")
        self.status_label.setText("✅ yt-dlp готов к работе")
        self.link_input.setFocus()
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        # Останавливаем все потоки перед закрытием
        if self.info_thread and self.info_thread.isRunning():
            self.info_thread.terminate()
            self.info_thread.wait()
        
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        
        if self.size_thread and self.size_thread.isRunning():
            self.size_thread.terminate()
            self.size_thread.wait()
        
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    # Настройка стиля приложения
    app.setStyle('Fusion')
    
    window = LinkInputWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
