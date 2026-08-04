#!/usr/bin/env python3
"""CLI del compilador EverforestAdwaita - usa el compilador modular."""
import sys
from pathlib import Path

# Añadir src/compiler al path
sys.path.insert(0, str(Path(__file__).parent / "compiler"))

from compiler.build import build_theme


def compile_sass(theme_name):
    import sass
    theme_path = Path(__file__).parent / "themes" / theme_name
    scss_file = theme_path / "sass" / "overrides.scss"
    css_file = theme_path / "overrides.css"
    if scss_file.exists():
        print(f"Compilando overrides de Sass ({scss_file.name}) -> {css_file.name}...")
        try:
            compiled_css = sass.compile(
                filename=str(scss_file),
                output_style='expanded'
            )
            with open(css_file, "w", encoding="utf-8") as f:
                f.write(compiled_css)
            print("-> Compilación de Sass exitosa.")
        except Exception as e:
            print(f"ERROR al compilar Sass: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compilar tema EverforestAdwaita")
    parser.add_argument("--theme", default="everforest-adwaita", help="Nombre del tema en src/themes/")
    parser.add_argument("--gtk3", action="store_true", help="Compilar solo GTK 3")
    parser.add_argument("--gtk4", action="store_true", help="Compilar solo GTK 4")
    args = parser.parse_args()

    compile_sass(args.theme)

    do_gtk3 = args.gtk3 or (not args.gtk3 and not args.gtk4)
    do_gtk4 = args.gtk4 or (not args.gtk3 and not args.gtk4)

    build_theme(args.theme, do_gtk3, do_gtk4)


if __name__ == "__main__":
    main()