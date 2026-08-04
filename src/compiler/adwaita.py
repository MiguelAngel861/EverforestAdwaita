#!/usr/bin/env python3
"""Extracción de CSS base y assets de Adwaita desde GResources."""
import os
import json
import hashlib
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class AdwaitaBase:
    css_content: str
    gtk_version: str
    css_hash: str


GTK3_RESOURCE_PREFIX = "/org/gtk/libgtk/theme/Adwaita"
GTK4_RESOURCE_PREFIX = "/org/gtk/libgtk/theme/Default"

GTK3_CSS_RESOURCE = f"{GTK3_RESOURCE_PREFIX}/gtk-contained-dark.css"
GTK4_CSS_RESOURCE = f"{GTK4_RESOURCE_PREFIX}/Default-dark.css"

GTK3_ASSETS_PREFIX = f"{GTK3_RESOURCE_PREFIX}/assets"
GTK4_ASSETS_PREFIX = f"{GTK4_RESOURCE_PREFIX}/assets"

CACHE_DIR = Path(__file__).parent.parent.parent / "build" / "cache"


def compute_hash(content: str) -> str:
    """Calcula SHA256 del contenido."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def extract_css_base(gtk_version: str) -> AdwaitaBase:
    """Extrae el CSS base de Adwaita para la versión GTK especificada."""
    if gtk_version == "3":
        gi_version = "3.0"
        css_resource = GTK3_CSS_RESOURCE
    elif gtk_version == "4":
        gi_version = "4.0"
        css_resource = GTK4_CSS_RESOURCE
    else:
        raise ValueError(f"Versión GTK no soportada: {gtk_version}")

    # Usar subprocess para aislar la versión de GTK (no se pueden cargar 3 y 4 en mismo proceso)
    py_code = f"""
import gi, sys, json
gi.require_version('Gtk', '{gi_version}')
from gi.repository import Gtk, Gio
Gtk.init()
try:
    bytes_data = Gio.resources_lookup_data('{css_resource}', Gio.ResourceLookupFlags.NONE)
    css_content = bytes_data.get_data().decode('utf-8')
    version = f"{{Gtk.get_major_version()}}.{{Gtk.get_minor_version()}}.{{Gtk.get_micro_version()}}"
    print(json.dumps({{"success": True, "css": css_content, "version": version}}))
except Exception as e:
    print(json.dumps({{"success": False, "error": str(e)}}))
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", py_code], capture_output=True, text=True, check=False)
    data = json.loads(result.stdout.strip())
    if not data["success"]:
        raise RuntimeError(f"Error extrayendo CSS base GTK {gtk_version}: {data['error']}")

    css_content = data["css"]
    version = data["version"]
    css_hash = compute_hash(css_content)

    return AdwaitaBase(css_content=css_content, gtk_version=version, css_hash=css_hash)


def extract_assets(gtk_version: str, output_dir: Path) -> None:
    """Extrae los assets de Adwaita al directorio especificado."""
    if gtk_version == "3":
        gi_version = "3.0"
        assets_prefix = GTK3_ASSETS_PREFIX
    elif gtk_version == "4":
        gi_version = "4.0"
        assets_prefix = GTK4_ASSETS_PREFIX
    else:
        raise ValueError(f"Versión GTK no soportada: {gtk_version}")

    py_code = f"""
import gi, os, json, sys
gi.require_version('Gtk', '{gi_version}')
from gi.repository import Gtk, Gio
Gtk.init()

assets_dir = os.path.join('{output_dir}', "assets")
os.makedirs(assets_dir, exist_ok=True)

try:
    children = Gio.resources_enumerate_children('{assets_prefix}', Gio.ResourceLookupFlags.NONE)
    for child in children:
        if not child.endswith('/'):
            res_path = f'{assets_prefix}/{{child}}'
            data = Gio.resources_lookup_data(res_path, Gio.ResourceLookupFlags.NONE).get_data()
            with open(os.path.join(assets_dir, child), "wb") as f:
                f.write(data)
    print(json.dumps({{"success": True, "count": len([c for c in children if not c.endswith('/')])}}))
except Exception as e:
    print(json.dumps({{"success": False, "error": str(e)}}))
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", py_code], capture_output=True, text=True, check=False)
    data = json.loads(result.stdout.strip())
    if not data["success"]:
        print(f"Advertencia al extraer assets GTK {gtk_version}: {data['error']}", file=sys.stderr)
    else:
        print(f"-> Assets de GTK {gtk_version} extraídos correctamente ({data['count']} archivos).")


def load_cached_base(gtk_version: str) -> Optional[AdwaitaBase]:
    """Carga el CSS base desde cache si existe."""
    cache_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.css"
    meta_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.meta.json"
    if cache_file.exists() and meta_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            css_content = f.read()
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return AdwaitaBase(css_content=css_content, gtk_version=meta["version"], css_hash=meta["hash"])
    return None


def save_base_cache(base: AdwaitaBase, gtk_version: str) -> None:
    """Guarda el CSS base en cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.css"
    meta_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.meta.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(base.css_content)
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({"version": base.gtk_version, "hash": base.css_hash}, f, indent=2)


def check_base_changed(base: AdwaitaBase, gtk_version: str) -> bool:
    """Compara el base actual con el cache y genera diff si cambió."""
    cached = load_cached_base(gtk_version)
    if cached is None:
        return True
    if cached.css_hash != base.css_hash:
        # Generar diff
        diff_file = CACHE_DIR / f"diff-gtk{gtk_version}.patch"
        old_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.old.css"
        with open(old_file, "w", encoding="utf-8") as f:
            f.write(cached.css_content)
        new_file = CACHE_DIR / f"adwaita-gtk{gtk_version}.new.css"
        with open(new_file, "w", encoding="utf-8") as f:
            f.write(base.css_content)
        import difflib
        diff = list(difflib.unified_diff(
            cached.css_content.splitlines(keepends=True),
            base.css_content.splitlines(keepends=True),
            fromfile="cached",
            tofile="current",
            lineterm=""
        ))
        if diff:
            with open(diff_file, "w", encoding="utf-8") as f:
                f.writelines(diff)
            print(f"AVISO: CSS base de Adwaita GTK {gtk_version} cambió (ver {diff_file})")
        return True
    return False