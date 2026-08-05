#!/usr/bin/env python3
"""CLI del compilador EverforestAdwaita - usa el compilador modular."""
import sys
from pathlib import Path

# Añadir src/compiler al path
sys.path.insert(0, str(Path(__file__).parent / "compiler"))

from compiler.build import build_theme


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compilar tema EverforestAdwaita")
    parser.add_argument("--theme", default="everforest-adwaita", help="Nombre del tema en src/themes/")
    parser.add_argument("--gtk3", action="store_true", help="Compilar solo GTK 3")
    parser.add_argument("--gtk4", action="store_true", help="Compilar solo GTK 4")
    args = parser.parse_args()

    do_gtk3 = args.gtk3 or (not args.gtk3 and not args.gtk4)
    do_gtk4 = args.gtk4 or (not args.gtk3 and not args.gtk4)

    build_theme(args.theme, do_gtk3, do_gtk4)


if __name__ == "__main__":
    main()