import os
import subprocess
import sys
import venv
import platform

import ssl

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
# ...existing code...

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, "venv_ytdlp")
PYTHON_BIN = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "python")
PIP_BIN = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
YT_DLP_BIN = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "yt-dlp")
DOWNLOAD_DIR = SCRIPT_DIR

WATCHED_FILE = os.path.join(DOWNLOAD_DIR, ".watched.txt")
DEFAULT_PLAYER = "vlc"  # Change to your preferred player like "mpv", "smplayer", etc.


def create_venv():
    if not os.path.exists(VENV_DIR):
        print("[+] Creating virtual environment...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
        subprocess.run([PYTHON_BIN, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.run([PIP_BIN, "install", "yt-dlp[default,curl-cffi]", "certifi"])


def update_dependencies():
    print("[+] Updating yt-dlp...")
    subprocess.run([PIP_BIN, "install", "--upgrade", "yt-dlp"])


def download_video():
    url = input("Enter YouTube URL (video/playlist/channel): ").strip()
    if not url:
        print("[!] No URL entered.")
        return

    # Use yt-dlp template variables for playlist/channel
    # %(uploader)s for channel, %(playlist)s for playlist, fallback to main dir if not present
    output_template = os.path.join(
        DOWNLOAD_DIR,
        "%(uploader|playlist)s",  # Use uploader (channel) or playlist as folder
        "%(title)s.%(ext)s"
    )

    # Ensure parent directory exists (yt-dlp will create it, but for safety)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    subprocess.run([YT_DLP_BIN, "--extractor-args", "generic:impersonate", "-o", output_template, url])


def load_watched():
    if os.path.exists(WATCHED_FILE):
        with open(WATCHED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    return set()


def save_watched(watched_set):
    with open(WATCHED_FILE, "w", encoding="utf-8") as f:
        for item in sorted(watched_set):
            f.write(item + "\n")


def browse_videos():
    watched = load_watched()

    def get_files():
        video_files = []
        for root, dirs, files in os.walk(DOWNLOAD_DIR):
            for f in files:
                if f.lower().endswith((".mp4", ".mkv", ".webm", ".flv", ".avi")):
                    # Store relative path from DOWNLOAD_DIR for display and watched tracking
                    rel_path = os.path.relpath(os.path.join(root, f), DOWNLOAD_DIR)
                    video_files.append(rel_path)
        return sorted(video_files)

    sort_unwatched = False

    while True:
        files = get_files()
        if sort_unwatched:
            files.sort(key=lambda x: (x in watched, x.lower()))  # Unwatched first

        print("\n==== Video Browser ====")
        for i, f in enumerate(files, 1):
            status = "[✓]" if f in watched else "[ ]"
            print(f"{i:2d}. {status} {f}")
        print("\ns. Search  p. Play  d. Delete  w. Toggle Watched  u. Toggle Unwatched Sort  q. Back")

        action = input("Choose action (s/p/d/w/u/q): ").lower()

        if action == 'q':
            save_watched(watched)
            break

        elif action == 's':
            keyword = input("Enter search term: ").lower()
            results = [f for f in files if keyword in f.lower()]
            if results:
                print("\nSearch Results:")
                for f in results:
                    status = "[✓]" if f in watched else "[ ]"
                    print(f"- {status} {f}")
            else:
                print("No matches found.")

        elif action == 'u':
            sort_unwatched = not sort_unwatched
            print(f"[+] Sort by unwatched: {'Enabled' if sort_unwatched else 'Disabled'}")

        elif action in ['p', 'd', 'w']:
            try:
                idx = int(input("Enter video number: "))
                if not (1 <= idx <= len(files)):
                    print("[!] Invalid number.")
                    continue
                rel_path = files[idx - 1]
                fullpath = os.path.join(DOWNLOAD_DIR, rel_path)

                if action == 'p':
                    try:
                        subprocess.run([DEFAULT_PLAYER, fullpath])
                    except FileNotFoundError:
                        print(f"[!] Player '{DEFAULT_PLAYER}' not found.")

                elif action == 'd':
                    confirm = input(f"Are you sure you want to delete '{rel_path}'? (y/n): ").lower()
                    if confirm == 'y':
                        os.remove(fullpath)
                        watched.discard(rel_path)
                        print("[+] File deleted.")

                elif action == 'w':
                    if rel_path in watched:
                        watched.remove(rel_path)
                        print(f"[ ] Unmarked: {rel_path}")
                    else:
                        watched.add(rel_path)
                        print(f"[✓] Marked as watched: {rel_path}")

            except ValueError:
                print("[!] Please enter a valid number.")

def main_menu():
    while True:
        print("\n==== YouTube Downloader ====")
        print("1. Download Video/Playlist/Channel")
        print("2. Update yt-dlp")
        print("3. Exit")
        print("4. Browse Downloaded Videos")

        choice = input("Select an option: ").strip()
        if choice == "1":
            download_video()
        elif choice == "2":
            update_dependencies()
        elif choice == "3":
            print("Goodbye!")
            break
        elif choice == "4":
            browse_videos()
        else:
            print("[!] Invalid option. Try again.")


if __name__ == "__main__":
    create_venv()
    main_menu()