#!/usr/bin/env python3
"""Carga y validación de configuración de tema."""
import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ThemeConfig:
    name: str
    display_name: str
    description: str
    version: str
    palette: str
    base_theme: str
    gtk_versions: Dict[str, str]
    files: Dict[str, str]
    features: list
    requirements: Dict[str, str]
    colors_map: Dict[str, str]
    palette_colors: Dict[str, str]
    theme_dir: Optional[Path] = field(default=None)

    def resolve(self, rel_path: str) -> Path:
        """Resuelve una ruta relativa al directorio del tema."""
        if self.theme_dir is None:
            raise RuntimeError("theme_dir no establecido")
        return self.theme_dir / rel_path

    @property
    def colors_path(self) -> str:
        return self.files["colors"]

    @property
    def overrides_path(self) -> str:
        return self.files["overrides"]

    @property
    def overrides_gtk4_path(self) -> Optional[str]:
        return self.files.get("overrides_gtk4")

    @property
    def overrides_gtk3_path(self) -> Optional[str]:
        return self.files.get("overrides_gtk3")


def load_theme(theme_dir: Path) -> ThemeConfig:
    """Carga theme.json y colors.json, valida estructura."""
    theme_json_path = theme_dir / "theme.json"
    if not theme_json_path.exists():
        raise FileNotFoundError(f"theme.json no encontrado en {theme_dir}")

    with open(theme_json_path, "r", encoding="utf-8") as f:
        theme_data = json.load(f)

    colors_path = theme_dir / theme_data["files"]["colors"]
    if not colors_path.exists():
        raise FileNotFoundError(f"colors.json no encontrado en {colors_path}")

    with open(colors_path, "r", encoding="utf-8") as f:
        colors_data = json.load(f)

    colors_map = colors_data.get("map", colors_data)
    palette_colors = colors_data.get("palette", {})

    return ThemeConfig(
        name=theme_data["name"],
        display_name=theme_data["display_name"],
        description=theme_data["description"],
        version=theme_data["version"],
        palette=theme_data["palette"],
        base_theme=theme_data["base_theme"],
        gtk_versions=theme_data["gtk_versions"],
        files=theme_data["files"],
        features=theme_data["features"],
        requirements=theme_data["requirements"],
        colors_map=colors_map,
        palette_colors=palette_colors,
        theme_dir=theme_dir,
    )