#!/usr/bin/env python3
"""Auto-compile watcher for EverforestAdwaita theme.

Monitors src/themes/ (colors.json, overrides*.css, theme.json) and
src/compiler/ for changes and runs 'make compile'.
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

WATCHED_EXTENSIONS = {".json", ".css", ".py"}


class ThemeChangeHandler(FileSystemEventHandler):
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.last_compile = 0.0

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix not in WATCHED_EXTENSIONS:
            return
        # Solo vigilar temas y el compilador (no tests/ ni docs/)
        if self.src_dir not in path.parents and path.parent != self.src_dir:
            return
        now = time.time()
        if now - self.last_compile > 1.0:  # debounce
            self.last_compile = now
            print(f"[{time.strftime('%H:%M:%S')}] Change in {path.relative_to(self.src_dir.parent)} -> compiling...", flush=True)
            result = subprocess.run(['make', 'compile'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[{time.strftime('%H:%M:%S')}] Compile OK", flush=True)
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Compile FAILED:\n{result.stderr}", flush=True)


def main():
    repo_root = Path(__file__).parent.parent
    src_dir = repo_root / 'src'
    if not src_dir.exists():
        print(f"Error: src directory not found at {src_dir}", flush=True)
        sys.exit(1)

    print(f"Watching {src_dir} (themes y compiler)...", flush=True)
    print("Press Ctrl+C to stop", flush=True)

    handler = ThemeChangeHandler(src_dir)
    observer = Observer()
    observer.schedule(handler, str(src_dir / 'themes'), recursive=True)
    observer.schedule(handler, str(src_dir / 'compiler'), recursive=True)
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