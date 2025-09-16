# 🚀 Быстрый старт

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/USERNAME/youtube-video-downloader.git
cd youtube-video-downloader
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Установка FFmpeg (для объединения video-only форматов)

**Windows:**
1. Скачайте с https://ffmpeg.org/download.html
2. Распакуйте в `C:\ffmpeg`
3. Добавьте `C:\ffmpeg\bin` в PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

**macOS:**
```bash
brew install ffmpeg
```

### 4. Проверка установки
```bash
python test_installation.py
```

### 5. Запуск приложения
```bash
python main.py
```

## Использование

1. **Введите ссылку** на YouTube видео
2. **Выберите папку** для скачивания (опционально)
3. **Нажмите "Получить информацию"**
4. **Выберите формат** из списка
5. **Нажмите "Скачать"**

## Типы форматов

- 🎬 **Video+Audio** - скачивание напрямую
- 🎥 **Video Only** - скачивание видео + аудио + объединение в MP4
- 🎵 **Audio Only** - скачивание только аудио

## Возможности

- ✅ Выбор качества видео
- ✅ Отображение размера файла
- ✅ Выбор папки для скачивания
- ✅ Автоматическое объединение video-only форматов
- ✅ Современный GUI интерфейс
- ✅ Многопоточное скачивание

## Решение проблем

См. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Полная документация

См. [README.md](README.md)
