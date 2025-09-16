# 🚀 Quick Start

## Installation and Running

### 1. Clone Repository
```bash
git clone https://github.com/USERNAME/youtube-video-downloader.git
cd youtube-video-downloader
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (for merging video-only formats)

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

**macOS:**
```bash
brew install ffmpeg
```

### 4. Check Installation
```bash
python test_installation.py
```

### 5. Run App
```bash
python main.py
```

## Usage

1. **Enter URL** Enter YouTube video URL
2. **Select folder** (optional)
3. **Click "Get Info"**
4. **Choose format** from list
5. **Click "Download"**

## Format Types

- 🎬 **Video+Audio** - direct download
- 🎥 **Video Only** - video + audio + merge to MP4
- 🎵 **Audio Only** - audio only download

## Features

- ✅ Quality selection
- ✅ File size display
- ✅ Folder selection
- ✅ Auto-merge of video-only formats
- ✅ Modern GUI
- ✅ Multithreaded download

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Full Documentation

See [README.md](README.md)

