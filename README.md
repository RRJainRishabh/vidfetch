# YouTube Downloader (yt-dlp + Python)

A terminal-based YouTube/Playlist/Channel downloader and video browser built with Python and `yt-dlp`. Supports auto-virtual environment creation, download organization, and watched-status tracking.

## 📦 Features

- Automatic virtual environment setup (`venv_ytdlp`)
- Downloads single videos, playlists, or entire channels
- Organized folder structure (`%(uploader|playlist)s`)
- Integrated video browser with:
  - Playback
  - Delete
  - Mark as watched/unwatched
  - Search and sort by watched status
- Customizable default video player (e.g. VLC, MPV, etc.)

## 🛠 Setup Instructions

### 1. Clone or Download

```bash
git clone https://github.com/RRJainRishabh/vidfetch.git
cd vidfetch
```

### 2. Run the Script

The script will auto-create a virtual environment (`venv_ytdlp`) and install required dependencies.

```bash
python3 main.py
```

## ▶️ Usage

Choose the appropriate option to download or manage your videos.

> **Note:** Default player is set to `vlc`. Change `DEFAULT_PLAYER` in the script if needed.

## 📁 Download Folder Structure

Downloaded videos are organized automatically by:

- Channel (uploader)
- Playlist (if applicable)

## 🧾 Requirements

- Python 3.7+
- Internet connection
- VLC (or any other video player you set)

## ✅ To-Do / Future Plans

- GUI interface (optional)
- Add support for download queue
- JSON metadata viewer

## 📄 License

MIT License
