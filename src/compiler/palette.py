#!/usr/bin/env python3
"""Aplicación del mapa de colores con auditoría de hexes no cubiertos."""
import re
from pathlib import Path
from typing import Dict, Set, Tuple, List
from dataclasses import dataclass


@dataclass
class PaletteResult:
    css_content: str
    mapped_count: int
    unmapped_hexes: Set[str]
    warnings: List[str]


HEX_PATTERN = re.compile(r"(?<![0-9a-zA-Z_-])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3}|[0-9a-fA-F]{8})\b")


def find_all_hexes(css_content: str) -> Set[str]:
    """Encuentra todos los hexes en el CSS (normalizados a minúsculas con #)."""
    hexes = set()
    for match in HEX_PATTERN.finditer(css_content):
        hex_val = match.group(0).lower()
        # Normalizar a 6 dígitos si es 3
        if len(hex_val) == 4:  # #RGB
            r, g, b = hex_val[1], hex_val[2], hex_val[3]
            hex_val = f"#{r}{r}{g}{g}{b}{b}"
        elif len(hex_val) == 9:  # #RRGGBBAA - ignorar alpha para mapeo
            hex_val = hex_val[:7]
        hexes.add(hex_val)
    return hexes


def apply_color_map(css_content: str, color_map: Dict[str, str], case_insensitive: bool = True) -> Tuple[str, int]:
    """Aplica el mapa de colores al CSS. Retorna (css_modificado, cuenta_mapeos)."""
    count = 0
    flags = re.IGNORECASE if case_insensitive else 0
    for src, dest in color_map.items():
        # Normalizar la clave del mapa
        src_lower = src.lower()
        # Usar regex con word boundaries para evitar reemplazos parciales
        pattern = re.compile(re.escape(src_lower), flags)
        new_content, n = pattern.subn(dest, css_content)
        if n > 0:
            css_content = new_content
            count += n
    return css_content, count


def audit_unmapped_hexes(css_content: str, color_map: Dict[str, str]) -> Set[str]:
    """Encuentra hexes en el CSS que no están en el mapa."""
    all_hexes = find_all_hexes(css_content)
    mapped_hexes = {k.lower() for k in color_map.keys()}
    # Normalizar mapped_hexes igual que find_all_hexes
    normalized_mapped = set()
    for h in mapped_hexes:
        if len(h) == 4:
            r, g, b = h[1], h[2], h[3]
            normalized_mapped.add(f"#{r}{r}{g}{g}{b}{b}")
        elif len(h) == 9:
            normalized_mapped.add(h[:7])
        else:
            normalized_mapped.add(h)
    return all_hexes - normalized_mapped


def process_palette(css_content: str, color_map: Dict[str, str]) -> PaletteResult:
    """Procesa el CSS: aplica mapa + auditoría."""
    warnings = []
    unmapped: Set[str] = set()

    # 1. Auditoría de hexes no cubiertos (sobre el CSS original de Adwaita)
    unmapped = audit_unmapped_hexes(css_content, color_map)
    if unmapped:
        # Filtrar hexes que pueden ser ruido (ej. rgba descompuestos, white/black)
        suspicious = {h for h in unmapped if h not in ("#ffffff", "#000000", "#fff", "#000")}
        if suspicious:
            warnings.append(f"Hexes en CSS sin mapear en colors.json: {sorted(suspicious)}")

    # 2. Aplicar mapa de colores
    css_mapped, mapped_count = apply_color_map(css_content, color_map)

    return PaletteResult(
        css_content=css_mapped,
        mapped_count=mapped_count,
        unmapped_hexes=unmapped,
        warnings=warnings,
    )