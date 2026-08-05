#!/usr/bin/env python3
"""Ensamblaje final: Compilación autónoma con Sass de Adwaita forkeado."""
import os
import sys
import shutil
from pathlib import Path
import sass

from .theme import ThemeConfig, load_theme


def compile_gtk(theme: ThemeConfig, gtk_version: str, output_dir: Path) -> None:
    """Compila el tema autónomo de forma nativa utilizando Sass de Adwaita."""
    print(f"Compilando tema GTK {gtk_version} desde fuentes SCSS...")

    theme_dir = Path(theme.theme_dir)

    # 1. Determinar rutas del punto de entrada Sass y destino
    if gtk_version == "3":
        scss_entry = theme_dir / "sass-gtk3" / "gtk-contained-dark.scss"
        src_assets = theme_dir / "sass-gtk3" / "assets"
    elif gtk_version == "4":
        scss_entry = theme_dir / "sass-gtk4" / "Default-dark.scss"
        src_assets = theme_dir / "sass-gtk4" / "assets"
    else:
        raise ValueError(f"Versión GTK no soportada: {gtk_version}")

    if not scss_entry.exists():
        print(f"Error: No se encontró el punto de entrada SCSS en {scss_entry}", file=sys.stderr)
        sys.exit(1)

    # 2. Compilar el SCSS a CSS final
    try:
        final_css = sass.compile(
            filename=str(scss_entry),
            output_style='expanded'
        )
    except Exception as e:
        print(f"ERROR de compilación Sass para GTK {gtk_version}: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Escribir salida (gtk.css y gtk-dark.css)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "gtk.css", "w", encoding="utf-8") as f:
        f.write(final_css)

    with open(output_dir / "gtk-dark.css", "w", encoding="utf-8") as f:
        f.write('@import url("gtk.css");\n')

    # 4. Copiar assets locales
    dest_assets = output_dir / "assets"
    if src_assets.exists():
        if dest_assets.exists():
            shutil.rmtree(dest_assets)
        shutil.copytree(src_assets, dest_assets)
        print(f"-> Assets de GTK {gtk_version} copiados correctamente.")

    print(f"-> GTK {gtk_version} compilado correctamente.")


def build_theme(theme_name: str = "everforest-adwaita", gtk3: bool = True, gtk4: bool = True) -> None:
    """Punto de entrada principal para compilar un tema."""
    src_dir = Path(__file__).parent.parent
    theme_dir = src_dir / "themes" / theme_name
    output_root = src_dir.parent

    if not theme_dir.exists():
        print(f"Error: Tema no encontrado: {theme_dir}")
        sys.exit(1)

    theme = load_theme(theme_dir)

    if gtk3:
        compile_gtk(theme, "3", output_root / "gtk-3.0")
    if gtk4:
        compile_gtk(theme, "4", output_root / "gtk-4.0")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compilar tema EverforestAdwaita")
    parser.add_argument("--theme", default="everforest-adwaita", help="Nombre del tema en src/themes/")
    parser.add_argument("--gtk3", action="store_true", help="Compilar solo GTK 3")
    parser.add_argument("--gtk4", action="store_true", help="Compilar solo GTK 4")
    parser.add_argument("--both", action="store_true", help="Compilar ambos (default)")
    args = parser.parse_args()

    do_gtk3 = args.gtk3 or args.both or (not args.gtk3 and not args.gtk4)
    do_gtk4 = args.gtk4 or args.both or (not args.gtk3 and not args.gtk4)

    build_theme(args.theme, do_gtk3, do_gtk4)