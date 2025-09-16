# 🎬 YouTube Video Downloader

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-green.svg)](https://pypi.org/project/PyQt5/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2023.12.30-red.svg)](https://pypi.org/project/yt-dlp/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)

Полнофункциональное PyQt5 приложение для скачивания видео с YouTube с использованием yt-dlp.

## Возможности

- 🎥 **Скачивание видео с YouTube** - поддержка всех форматов
- 📋 **Выбор качества** - автоматическое определение доступных форматов
- 🔄 **Умное объединение** - video-only форматы автоматически объединяются с лучшим аудио
- 📁 **Выбор папки** - возможность выбрать папку для скачивания
- 🎬 **Три типа скачивания**:
  - **Video+Audio** - скачивание напрямую
  - **Video Only** - скачивание видео + аудио + объединение
  - **Audio Only** - скачивание только аудио
- 📊 **Отображение размера** - показывает размер файла при выборе формата
- 🎨 **Современный интерфейс** - удобный GUI с прогресс-баром
- ⚡ **Многопоточность** - скачивание не блокирует интерфейс
- 🛡️ **Обработка ошибок** - полная валидация и обработка ошибок

## 🚀 Быстрый старт

### Клонирование и установка
```bash
git clone https://github.com/USERNAME/youtube-video-downloader.git
cd youtube-video-downloader
pip install -r requirements.txt
```

### Установка FFmpeg
- **Windows**: [Скачать](https://ffmpeg.org/download.html) и добавить в PATH
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Запуск
```bash
python main.py
```

## 📦 Установка

1. Убедитесь, что у вас установлен Python 3.6 или выше
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

### GUI приложение (рекомендуется):
```bash
python main.py
```

### Консольная версия:
```bash
python youtube_downloader.py
```

## Использование GUI

1. **Запустите приложение** - `python main.py`
2. **Введите ссылку** на YouTube видео в поле ввода
3. **Выберите папку** для скачивания (по умолчанию - текущая папка)
4. **Нажмите "Получить информацию"** - приложение получит данные о видео
5. **Выберите формат** из выпадающего списка (качество, тип, расширение)
6. **Нажмите "Скачать"** - видео будет скачано в выбранную папку

### 📁 Где найти скачанные файлы

- **По умолчанию**: файлы скачиваются в папку с приложением
- **Выбор папки**: нажмите кнопку "Выбрать папку" для выбора другой папки
- **Имя файла**: автоматически генерируется из названия видео
- **Формат**: MP4 (для объединенных файлов) или оригинальный формат

## Использование консольной версии

1. **Запустите скрипт** - `python youtube_downloader.py`
2. **Введите URL** видео при запросе
3. **Выберите формат** по ID из списка
4. **Дождитесь завершения** скачивания

## Поддерживаемые форматы

- **Video+Audio** - полное видео с звуком
- **Video Only** - только видео (автоматически объединяется с лучшим аудио)
- **Audio Only** - только аудио

## Технические детали

- **yt-dlp** - для скачивания видео
- **PyQt5** - для графического интерфейса
- **subprocess** - для запуска yt-dlp
- **re** - для парсинга форматов
- **QThread** - для многопоточного скачивания

## Требования

- Python 3.6+
- yt-dlp
- PyQt5
- FFmpeg (для объединения video-only форматов)
- Интернет-соединение

### Установка FFmpeg

**Windows:**
1. Скачайте FFmpeg с https://ffmpeg.org/download.html
2. Распакуйте в папку (например, `C:\ffmpeg`)
3. Добавьте `C:\ffmpeg\bin` в PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

**macOS:**
```bash
brew install ffmpeg
```

## Обработка ошибок

Приложение автоматически:
- Проверяет установку yt-dlp и FFmpeg при запуске
- Показывает статус готовности в интерфейсе
- Предупреждает о проблемах с FFmpeg для video-only форматов
- Валидирует URL видео
- Обрабатывает ошибки сети
- Показывает понятные сообщения об ошибках

### Проверка установки

```bash
python test_installation.py  # Проверка всех зависимостей
python check_ffmpeg.py       # Проверка только FFmpeg
```

## 📚 Документация

- [QUICK_START.md](QUICK_START.md) - Быстрый старт
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Настройка GitHub
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Решение проблем

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🙏 Благодарности

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - за отличную библиотеку для скачивания
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - за GUI фреймворк
- [FFmpeg](https://ffmpeg.org/) - за инструменты для обработки медиа
