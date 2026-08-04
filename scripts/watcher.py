#!/usr/bin/env python3
"""Auto-compile watcher for EverforestAdwaita theme.

Monitors src/colors.json and src/overrides.css for changes and runs 'make compile'.
"""
import subprocess
import time
import sys
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: 'watchdog' not installed. Install with: pip install watchdog", flush=True)
    sys.exit(1)


class ThemeChangeHandler(FileSystemEventHandler):
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.last_compile = 0.0

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.name in ('colors.json', 'overrides.css') and path.parent == self.src_dir:
            now = time.time()
            if now - self.last_compile > 1.0:  # debounce
                self.last_compile = now
                print(f"[{time.strftime('%H:%M:%S')}] Change in {path.name} -> compiling...", flush=True)
                result = subprocess.run(['make', 'compile'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Compile OK", flush=True)
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Compile FAILED:\n{result.stderr}", flush=True)


def main():
    src_dir = Path(__file__).parent.parent / 'src'
    if not src_dir.exists():
        print(f"Error: src directory not found at {src_dir}", flush=True)
        sys.exit(1)

    print(f"Watching {src_dir} for changes to colors.json and overrides.css...", flush=True)
    print("Press Ctrl+C to stop", flush=True)

    handler = ThemeChangeHandler(src_dir)
    observer = Observer()
    observer.schedule(handler, str(src_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...", flush=True)
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()