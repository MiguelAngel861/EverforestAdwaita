#!/usr/bin/env python3
"""Script para recolorear de forma nativa los archivos vectoriales assets.svg."""
import re
from pathlib import Path

# Mapa de reemplazo de colores (de los azules de Adwaita a los verdes/gris de Everforest)
COLOR_REPLACEMENTS = {
    # GTK 3 & GTK 4 azules comunes
    "#3584e4": "#A7C080",  # Azul acento principal -> Verde Everforest
    "#2a76d9": "#8fbcbb",  # Azul hover
    "#215d9c": "#3C4841",  # Azul activo/oscuro -> Verde oscuro/backdrop
    "#1b6acb": "#3C4841",  # Azul oscuro
    "#3465a4": "#A7C080",  # Azul clásico de assets
    "#729fcf": "#A7C080",  # Azul claro
}

def recolor_svg(svg_path: Path):
    if not svg_path.exists():
        print(f"Aviso: No se encontró {svg_path}")
        return

    print(f"Recoloreando {svg_path.name}...")
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar colores (insensible a mayúsculas/minúsculas)
    replaced_count = 0
    for orig, dest in COLOR_REPLACEMENTS.items():
        pattern = re.compile(re.escape(orig), re.IGNORECASE)
        content, count = pattern.subn(dest, content)
        replaced_count += count

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"-> {svg_path.name} recoloreado ({replaced_count} ocurrencias reemplazadas).")


def main():
    src_dir = Path(__file__).parent
    theme_dir = src_dir / "theme"
    
    # SVG de GTK 3
    recolor_svg(theme_dir / "sass-gtk3" / "assets.svg")
    
    # SVG de GTK 4
    recolor_svg(theme_dir / "sass-gtk4" / "assets.svg")


if __name__ == "__main__":
    main()
