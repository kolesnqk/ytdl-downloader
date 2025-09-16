# 🎬 YouTube Video Downloader

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-green.svg)](https://pypi.org/project/PyQt5/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2023.12.30-red.svg)](https://pypi.org/project/yt-dlp/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)

A full-featured PyQt5 application for downloading videos from YouTube using yt-dlp.

## Features

- 🎥 **YouTube Video Download** - supports all formats
- 📋 **Quality Selection** - auto-detects available formats
- 🔄 **Smart Merging** - video-only formats automatically merge with the best available audio track during download
- 📁 **Folder Selection** - option to choose download folder
- 🎬 **Three Download Types**:
  - **Video+Audio** - video + audio + merge
  - **Video Only** - video only download
  - **Audio Only** - audio only download
- 📊 **Size Display** - shows file size when selecting format
- 🎨 **Modern Interface** - user-friendly GUI with progress bar
- ⚡ **Multithreading** - download doesn't block interface
- 🛡️ **Error Handling** - full validation and error management

## 🚀 Быстрый старт

### Cloning and Installation
```bash
git clone https://github.com/USERNAME/youtube-video-downloader.git
cd youtube-video-downloader
pip install -r requirements.txt
```

### Installing FFmpeg
- **Windows**: [Download](https://ffmpeg.org/download.html) and add to PATH
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Running
```bash
python main.py
```

## 📦 Installation

1. Ensure Python 3.6 or higher is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

### GUI Application (recommended):
```bash
python main.py
```

### Console Version:
```bash
python youtube_downloader.py
```

## Using GUI

1. **Run the app** - `python main.py`
2. **Enter URL** of YouTube video in input field
3. **Select folder** for download (default is current folder)
4. **Click "Get Info""** - app retrieves video data
5. **Choose format** from dropdown (quality, type, extension)
6. **Click "Download"** - video downloads to selected folder

### 📁 Where to Find Downloaded Files

- **Default**: files save to app folder
- **Folder Selection**: click "Choose Folder" to pick another
- **File Name**: auto-generated from video title
- **Format**: MP4 (for merged files) or original format

## Using Console Version

1. **Run script** - `python youtube_downloader.py`
2. **Enter URL** when prompted
3. **Select format** by ID from list
4. **Wait for download** to complete

## Supported Formats

- **Video+Audio** - full video with sound
- **Video Only** - video only (auto-merges with best audio)
- **Audio Only** - audio only

## Технические детали

- **yt-dlp** - for video downloading
- **PyQt5** - for GUI
- **subprocess** - for running yt-dlp
- **re** - for format parsing
- **QThread** - for multithreaded downloading

## Requirements

- Python 3.6+
- yt-dlp
- PyQt5
- FFmpeg (for merging video-only formats)
- Internet connection

### Installing FFmpeg

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

**macOS:**
```bash
brew install ffmpeg
```

## Error Handling

App automatically:
- Checks yt-dlp and FFmpeg installation on start
- Displays readiness status in interface
- Warns about FFmpeg issues for video-only formats
- Validates video URL
- Handles network errors
- Shows clear error messages

### Installation Check

```bash
python test_installation.py  # Check all dependencies
python check_ffmpeg.py       # Check only FFmpeg
```

## 📚 Documentation

- [QUICK_START.md](QUICK_START.md) - Quick Start
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub Setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting

## 🤝 Contributing

1. Fork the repository
2. Create branch for new feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is released under the MIT License. See 'LICENSE' file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - for excellent download library
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - for GUI framework
- [FFmpeg](https://ffmpeg.org/) - for media processing tools

