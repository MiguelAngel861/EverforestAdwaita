#!/usr/bin/env python3
import os
import re
import subprocess
import sys

# Rutas del tema
THEME_DIR = os.path.dirname(os.path.abspath(__file__))
GTK3_DIR = os.path.join(THEME_DIR, "gtk-3.0")
GTK4_DIR = os.path.join(THEME_DIR, "gtk-4.0")

# Mapeo de Colores: Adwaita Dark -> Everforest Dark Hard
COLOR_MAP = {
    # Fondos
    r'#353535': '#272E33',  # Fondo de ventana principal -> Everforest bg0
    r'#2d2d2d': '#1E2326',  # Fondo base de inputs/listas -> Everforest bg_dim
    r'#303030': '#2E383C',  # Fondo intermedio oscuro -> Everforest bg1
    r'#252525': '#1E2326',  # Fondo de barra de título -> Everforest bg_dim
    r'#282828': '#1E2326',  # Fondo oscuro alternativo -> Everforest bg_dim
    r'#2e2e2e': '#1E2326',  # Fondo oscuro alternativo -> Everforest bg_dim
    
    # Texto
    r'#eeeeec': '#D3C6AA',  # Color de texto -> Everforest fg
    
    # Deshabilitados / Insensibles
    r'#323232': '#2E383C',  # Fondo deshabilitado -> Everforest bg1
    r'#919190': '#9DA9A0',  # Texto deshabilitado -> Everforest grey2 (Mejora de contraste A11y: 4.84:1)
    r'#5b5b5b': '#7A8478',  # Bordes deshabilitados -> Everforest grey0
    
    # Bordes
    r'#1b1b1b': '#374145',  # Bordes principales -> Everforest bg2
    r'#202020': '#2E383C',  # Bordes desenfocados -> Everforest bg1
    
    # Selección y Acentuación (Azul -> Verde Everforest)
    r'#15539e': '#A7C080',  # Fondo de selección -> Everforest green
    r'#3584e4': '#A7C080',  # Fondo de selección alternativo -> Everforest green
    r'#1b6acb': '#A7C080',  # Fondo activo -> Everforest green
    r'#1f76e1': '#A7C080',  # Fondo check/radio checked -> Everforest green
    r'#3181e3': '#A7C080',  # Fondo check/radio checked hover -> Everforest green
    r'#1e74dd': '#A7C080',  # Fondo check/radio checked hover -> Everforest green
    r'#185cb0': '#A7C080',  # Focus/Active blue -> Everforest green
    r'#1961b9': '#A7C080',  # Focus/Active blue -> Everforest green
    r'#629fea': '#A7C080',  # Light blue selection/focus -> Everforest green
    
    # Bordes de selección y sombras oscuras
    r'#155099': '#3C4841',  # Borde de selección oscuro -> Everforest bg_green
    r'#1655a2': '#3C4841',  # Borde de selección -> Everforest bg_green
    r'#092444': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#0f3b71': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#103e75': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#143f73': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#16447c': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#194d8d': '#3C4841',  # Azul oscuro -> Everforest bg_green
    r'#2b62a6': '#3C4841',  # Azul medio -> Everforest bg_green
    r'#4f7aaf': '#3C4841',  # Azul medio -> Everforest bg_green
    r'#6885aa': '#3C4841',  # Azul medio -> Everforest bg_green
    r'#6a8bb5': '#3C4841',  # Azul medio -> Everforest bg_green
    r'#d7e6fa': '#3C4841',  # Fondo de selección muy claro -> Everforest bg_green
    r'#eff5fd': '#3C4841',  # Fondo de selección muy claro -> Everforest bg_green
    
    # Destacados en Aqua
    r'#a4c4ea': '#83C092',  # Azul suave -> Everforest aqua
    r'#b9cbe2': '#83C092',  # Azul suave -> Everforest aqua
    r'#d0ddec': '#83C092',  # Azul suave -> Everforest aqua
    
    # Grises azulados -> Grises Everforest
    r'#7398c5': '#859289',  # Gris azulado -> Everforest grey1
    r'#8aa9ce': '#859289',  # Gris azulado -> Everforest grey1
    r'#8ca6c6': '#859289',  # Gris azulado -> Everforest grey1
    r'#9cafc5': '#859289',  # Gris azulado -> Everforest grey1
    r'#a1b2c7': '#859289',  # Gris azulado -> Everforest grey1
    r'#d0dae5': '#859289',  # Gris azulado -> Everforest grey1
    
    # Estados del sistema
    r'#cc0000': '#E67E80',  # Error -> Everforest red
    r'#f57900': '#DBBC7F',  # Advertencia -> Everforest yellow
    r'#4e9a06': '#A7C080',  # Éxito -> Everforest green
}

# Reglas adicionales de estilo CSS
SUFFIX = """
/* --- OVERRIDES: Complete removal of rounded corners --- */
/* Forzamos esquinas completamente cuadradas (90 grados) en todos los elementos, incluyendo ventanas, diálogos, decoraciones y widgets */
* {
    border-radius: 0px;
    -gtk-outline-radius: 0px;
}

window,
dialog,
messagedialog,
decoration,
.decoration,
.window-frame,
windowdecoration,
headerbar,
.titlebar,
button,
entry,
notebook,
tab,
menu,
popover,
.card,
.sheet,
slider,
trough,
switch,
.sidebar,
list-row,
list,
treeview {
    border-radius: 0px;
}

/* --- OVERRIDES: High-contrast selection styling --- */
@define-color theme_selected_fg_color #1E2326;
@define-color theme_unfocused_selected_fg_color #1E2326;

:selected,
*:selected,
.selected,
list-row:selected,
treeview.view:selected,
entry selection,
label selection {
    color: #1E2326;
    background-color: #A7C080;
}

:selected label,
*:selected label,
.selected label,
list-row:selected label,
treeview.view:selected label,
:selected *,
*:selected *,
.selected *,
list-row:selected *,
treeview.view:selected * {
    color: #1E2326;
}

/* --- OVERRIDES: Backdrop state (Infocused windows selection contrast) --- */
:selected:backdrop,
*:selected:backdrop,
.selected:backdrop,
list-row:selected:backdrop {
    color: #D3C6AA;
    background-color: #3C4841;
}

:selected:backdrop label,
*:selected:backdrop label,
.selected:backdrop label,
list-row:selected:backdrop label,
:selected:backdrop *,
*:selected:backdrop *,
.selected:backdrop * {
    color: #D3C6AA;
}

/* --- OVERRIDES: Minimalist Scrollbars --- */
scrollbar trough {
    background-color: #1E2326;
    border: none;
}
scrollbar slider {
    background-color: #414C50; /* Everforest bg3 */
    border: 2px solid #1E2326;
    border-radius: 0px;
}
scrollbar slider:hover {
    background-color: #859289; /* Everforest grey1 */
}
scrollbar slider:active {
    background-color: #A7C080; /* Everforest green */
}

/* --- OVERRIDES: Semantic Action Buttons --- */
button.suggested-action {
    background-color: #A7C080; /* Everforest green */
    color: #1E2326;
    border: 1px solid #3C4841;
}
button.suggested-action:hover {
    background-color: #b5cfa3;
    color: #1E2326;
}
button.suggested-action:active {
    background-color: #98b073;
    color: #1E2326;
}

button.destructive-action {
    background-color: #E67E80; /* Everforest red */
    color: #1E2326;
    border: 1px solid #4C3739;
}
button.destructive-action:hover {
    background-color: #eb9496;
    color: #1E2326;
}
button.destructive-action:active {
    background-color: #d16e70;
    color: #1E2326;
}

/* --- OVERRIDES: Text Entries Focus --- */
entry:focus {
    border: 1px solid #A7C080;
    box-shadow: none;
}
"""

def compile_gtk3():
    print("Compilando tema GTK 3...")
    py_code = f"""
import re, os, gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
Gtk.init([])
try:
    bytes_data = Gio.resources_lookup_data('/org/gtk/libgtk/theme/Adwaita/gtk-contained-dark.css', Gio.ResourceLookupFlags.NONE)
    css_content = bytes_data.get_data().decode('utf-8')
    
    color_map = {repr(COLOR_MAP)}
    for src, dest in color_map.items():
        css_content = re.sub(src, dest, css_content, flags=re.IGNORECASE)
        
    css_content += {repr(SUFFIX)}
    
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
    py_code = f"""
import re, os, gi, sys
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
Gtk.init()
try:
    bytes_data = Gio.resources_lookup_data('/org/gtk/libgtk/theme/Default/Default-dark.css', Gio.ResourceLookupFlags.NONE)
    css_content = bytes_data.get_data().decode('utf-8')
    
    color_map = {repr(COLOR_MAP)}
    for src, dest in color_map.items():
        css_content = re.sub(src, dest, css_content, flags=re.IGNORECASE)
        
    css_content += {repr(SUFFIX)}
    
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
