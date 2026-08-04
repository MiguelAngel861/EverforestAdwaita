#!/usr/bin/env python3
"""Ensamblaje final: base mapeado + overrides → salida."""
import os
import json
import sys
from pathlib import Path
from typing import Optional

from .theme import ThemeConfig, load_theme
from .adwaita import (
    extract_css_base,
    extract_assets,
    save_base_cache,
    check_base_changed,
    AdwaitaBase,
)
from .palette import process_palette, PaletteResult


def compile_gtk(theme: ThemeConfig, gtk_version: str, output_dir: Path) -> None:
    """Compila el tema para una versión GTK específica."""
    print(f"Compilando tema GTK {gtk_version}...")

    # 1. Extraer CSS base de Adwaita (con cache y detección de cambios)
    base = extract_css_base(gtk_version)
    if check_base_changed(base, gtk_version):
        save_base_cache(base, gtk_version)

    # 2. Aplicar mapa de colores + auditoría
    palette_result: PaletteResult = process_palette(base.css_content, theme.colors_map)
    for w in palette_result.warnings:
        print(f"  ADVERTENCIA: {w}")

    # 3. Cargar overrides comunes
    overrides_path = theme.resolve(theme.overrides_path)
    with open(overrides_path, "r", encoding="utf-8") as f:
        overrides_css = f.read()

    # 4. Cargar overrides específicos de versión
    version_overrides = ""
    if gtk_version == "4" and theme.overrides_gtk4_path:
        overrides_gtk4_path = theme.resolve(theme.overrides_gtk4_path)
        if overrides_gtk4_path.exists():
            with open(overrides_gtk4_path, "r", encoding="utf-8") as f:
                version_overrides = f.read()
    elif gtk_version == "3" and theme.overrides_gtk3_path:
        overrides_gtk3_path = theme.resolve(theme.overrides_gtk3_path)
        if overrides_gtk3_path.exists():
            with open(overrides_gtk3_path, "r", encoding="utf-8") as f:
                version_overrides = f.read()

    # 5. Ensamblar CSS final
    final_css = palette_result.css_content + overrides_css + version_overrides

    # 6. Escribir salida
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"

    # 7. Extraer assets
    extract_assets(gtk_version, output_dir)

    # 8. Escribir gtk.css y gtk-dark.css
    with open(output_dir / "gtk.css", "w", encoding="utf-8") as f:
        f.write(final_css)

    with open(output_dir / "gtk-dark.css", "w", encoding="utf-8") as f:
        f.write('@import url("gtk.css");\n')

    print(f"-> GTK {gtk_version} compilado correctamente (mapeos: {palette_result.mapped_count}).")


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