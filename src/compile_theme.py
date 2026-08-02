#!/usr/bin/env python3
import os
import re
import json
import subprocess
import sys

# Rutas del tema
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_DIR = os.path.dirname(SRC_DIR)
GTK3_DIR = os.path.join(THEME_DIR, "gtk-3.0")
GTK4_DIR = os.path.join(THEME_DIR, "gtk-4.0")

# Cargar archivos de configuración
colors_path = os.path.join(SRC_DIR, "colors.json")
overrides_path = os.path.join(SRC_DIR, "overrides.css")

if not os.path.exists(colors_path):
    print(f"Error: No se encontró {colors_path}")
    sys.exit(1)

if not os.path.exists(overrides_path):
    print(f"Error: No se encontró {overrides_path}")
    sys.exit(1)

with open(colors_path, "r", encoding="utf-8") as f:
    COLOR_MAP = json.load(f)

with open(overrides_path, "r", encoding="utf-8") as f:
    SUFFIX = f.read()

def compile_gtk3():
    print("Compilando tema GTK 3...")
    color_map_str = json.dumps(COLOR_MAP)
    suffix_str = json.dumps(SUFFIX)
    
    py_code = f"""
import re, os, gi, sys, json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
Gtk.init([])
try:
    bytes_data = Gio.resources_lookup_data('/org/gtk/libgtk/theme/Adwaita/gtk-contained-dark.css', Gio.ResourceLookupFlags.NONE)
    css_content = bytes_data.get_data().decode('utf-8')
    
    color_map = json.loads({repr(color_map_str)})
    for src, dest in color_map.items():
        css_content = re.sub(src, dest, css_content, flags=re.IGNORECASE)
        
    suffix = json.loads({repr(suffix_str)})
    css_content += suffix
    
    # Extraer assets locales
    assets_dir = os.path.join({repr(GTK3_DIR)}, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    try:
        children = Gio.resources_enumerate_children('/org/gtk/libgtk/theme/Adwaita/assets', Gio.ResourceLookupFlags.NONE)
        for child in children:
            if not child.endswith('/'):
                res_path = f'/org/gtk/libgtk/theme/Adwaita/assets/{{child}}'
                data = Gio.resources_lookup_data(res_path, Gio.ResourceLookupFlags.NONE).get_data()
                with open(os.path.join(assets_dir, child), "wb") as f:
                    f.write(data)
        print("-> Assets de GTK 3 extraídos correctamente.")
    except Exception as e:
        print("Advertencia al extraer assets de GTK 3:", e)
        
    os.makedirs({repr(GTK3_DIR)}, exist_ok=True)
    with open(os.path.join({repr(GTK3_DIR)}, "gtk.css"), "w") as f:
        f.write(css_content)
        
    with open(os.path.join({repr(GTK3_DIR)}, "gtk-dark.css"), "w") as f:
        f.write('@import url(\"gtk.css\");\\n')
        
    print("-> GTK 3 compilado correctamente.")
except Exception as e:
    print("Error al compilar GTK 3:", e)
    sys.exit(1)
"""
    subprocess.run([sys.executable, "-c", py_code], check=True)

def compile_gtk4():
    print("Compilando tema GTK 4...")
    color_map_str = json.dumps(COLOR_MAP)
    suffix_str = json.dumps(SUFFIX)
    
    py_code = f"""
import re, os, gi, sys, json
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
Gtk.init()
try:
    bytes_data = Gio.resources_lookup_data('/org/gtk/libgtk/theme/Default/Default-dark.css', Gio.ResourceLookupFlags.NONE)
    css_content = bytes_data.get_data().decode('utf-8')
    
    color_map = json.loads({repr(color_map_str)})
    for src, dest in color_map.items():
        css_content = re.sub(src, dest, css_content, flags=re.IGNORECASE)
        
    suffix = json.loads({repr(suffix_str)})
    css_content += suffix
    
    # Extraer assets locales
    assets_dir = os.path.join({repr(GTK4_DIR)}, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    try:
        children = Gio.resources_enumerate_children('/org/gtk/libgtk/theme/Default/assets', Gio.ResourceLookupFlags.NONE)
        for child in children:
            if not child.endswith('/'):
                res_path = f'/org/gtk/libgtk/theme/Default/assets/{{child}}'
                data = Gio.resources_lookup_data(res_path, Gio.ResourceLookupFlags.NONE).get_data()
                with open(os.path.join(assets_dir, child), "wb") as f:
                    f.write(data)
        print("-> Assets de GTK 4 extraídos correctamente.")
    except Exception as e:
        print("Advertencia al extraer assets de GTK 4:", e)
        
    os.makedirs({repr(GTK4_DIR)}, exist_ok=True)
    with open(os.path.join({repr(GTK4_DIR)}, "gtk.css"), "w") as f:
        f.write(css_content)
        
    with open(os.path.join({repr(GTK4_DIR)}, "gtk-dark.css"), "w") as f:
        f.write('@import url(\"gtk.css\");\\n')
        
    print("-> GTK 4 compilado correctamente.")
except Exception as e:
    print("Error al compilar GTK 4:", e)
    sys.exit(1)
"""
    subprocess.run([sys.executable, "-c", py_code], check=True)

if __name__ == "__main__":
    compile_gtk3()
    compile_gtk4()
