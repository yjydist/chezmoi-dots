#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from hashlib import sha256

WALLPAPER_DIR = Path.home() / "Pictures/Wallpapers"
CACHE_DIR = Path.home() / ".cache/rofi-wallpaper"

def ensure_swww_daemon():
    if not any(p.name == "swww-daemon" for p in subprocess.run(["ps", "-eo", "comm"], capture_output=True, text=True).stdout.splitlines()):
        subprocess.Popen(["swww-daemon"])
        import time; time.sleep(0.3)

def generate_thumbnail(image_path: Path, thumb_path: Path):
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "convert", str(image_path),
        "-resize", "256x256^",
        "-gravity", "center",
        "-extent", "256x256",
        str(thumb_path)
    ], check=False)

def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ensure_swww_daemon()

    # 获取所有壁纸
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    wallpapers = [f for f in WALLPAPER_DIR.rglob("*") if f.suffix.lower() in extensions]
    wallpapers.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # 生成 Rofi 条目
    entries = []
    for wp in wallpapers:
        thumb = CACHE_DIR / (sha256(str(wp).encode()).hexdigest() + ".png")
        if not thumb.exists():
            generate_thumbnail(wp, thumb)
        entries.append(f"{wp.name}\0icon\x1f{thumb}")

    # 调用 Rofi
    result = subprocess.run(
        ["rofi", "-dmenu", "-theme", "~/.config/rofi/wallpaper.rasi", "-p", "🖼️ 选择壁纸:", "-sep", "\0", "-format", "d"],
        input="\n".join(entries),
        text=True,
        capture_output=True
    )

    if result.returncode == 1:  # 用户取消
        return

    try:
        index = int(result.stdout.strip())
        selected = wallpapers[index]
        subprocess.run([
            "swww", "img", str(selected),
            "--transition-type", "grow",
            "--transition-duration", "2"
        ])
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()