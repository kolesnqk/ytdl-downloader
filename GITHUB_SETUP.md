# Загрузка проекта на GitHub

## Шаг 1: Установка Git

### Windows:
1. Скачайте Git с https://git-scm.com/download/win
2. Установите с настройками по умолчанию
3. Перезапустите командную строку

### Альтернатива - GitHub Desktop:
1. Скачайте GitHub Desktop с https://desktop.github.com/
2. Установите и войдите в свой аккаунт GitHub

## Шаг 2: Инициализация Git репозитория

Откройте командную строку в папке проекта и выполните:

```bash
# Инициализация Git репозитория
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "Initial commit: YouTube Video Downloader with PyQt5"

# Настройка пользователя (если еще не настроено)
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```

## Шаг 3: Создание репозитория на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository" (зеленая кнопка)
3. Заполните:
   - **Repository name**: `youtube-video-downloader`
   - **Description**: `YouTube Video Downloader with PyQt5 GUI and yt-dlp`
   - **Visibility**: Public или Private (на ваш выбор)
   - **НЕ** добавляйте README, .gitignore или лицензию (у нас уже есть файлы)
4. Нажмите "Create repository"

## Шаг 4: Подключение к GitHub

```bash
# Добавление удаленного репозитория (замените USERNAME на ваш GitHub username)
git remote add origin https://github.com/USERNAME/youtube-video-downloader.git

# Переименование основной ветки в main
git branch -M main

# Загрузка на GitHub
git push -u origin main
```

## Шаг 5: Проверка

Зайдите на https://github.com/USERNAME/youtube-video-downloader и убедитесь, что все файлы загружены.

## Структура проекта

Ваш проект содержит:

```
youtube-video-downloader/
├── main.py                    # Основное GUI приложение
├── youtube_downloader.py      # Консольная версия
├── requirements.txt           # Зависимости Python
├── README.md                  # Документация
├── TROUBLESHOOTING.md         # Решение проблем
├── GITHUB_SETUP.md           # Эта инструкция
├── test_installation.py      # Проверка зависимостей
├── check_ffmpeg.py           # Проверка FFmpeg
├── test_ytdlp.py             # Тест yt-dlp
├── test_url.py               # Тест URL
├── test_pyqt.py              # Тест PyQt5
├── test_merge.py             # Тест объединения
├── test_manual_merge.py      # Тест ручного объединения
├── test_size_display.py      # Тест отображения размера
├── test_download_logic.py    # Тест логики скачивания
├── debug_main.py             # Отладка
└── show_downloads.py         # Показать скачанные файлы
```

## Дальнейшая работа

После загрузки на GitHub:

1. **Клонирование на других компьютерах**:
   ```bash
   git clone https://github.com/USERNAME/youtube-video-downloader.git
   cd youtube-video-downloader
   pip install -r requirements.txt
   python main.py
   ```

2. **Обновление проекта**:
   ```bash
   git add .
   git commit -m "Описание изменений"
   git push
   ```

3. **Создание релизов**:
   - Перейдите в раздел "Releases" на GitHub
   - Нажмите "Create a new release"
   - Добавьте тег версии (например, v1.0.0)
   - Добавьте описание изменений

## Полезные команды Git

```bash
# Проверка статуса
git status

# Просмотр изменений
git diff

# История коммитов
git log --oneline

# Отмена последнего коммита
git reset --soft HEAD~1

# Просмотр удаленных репозиториев
git remote -v
```

## Troubleshooting

### Ошибка "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/youtube-video-downloader.git
```

### Ошибка аутентификации:
- Используйте Personal Access Token вместо пароля
- Или настройте SSH ключи

### Конфлиты при push:
```bash
git pull origin main
# Разрешите конфликты
git add .
git commit -m "Resolve conflicts"
git push
```
