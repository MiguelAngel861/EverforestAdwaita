#!/usr/bin/env python3
"""Infraestructura compartida para los testers visuales de EverforestAdwaita.

Provee:
- parse_gtk_args(): argumentos --gtk3/--gtk4 con detección automática.
- css_path(): ruta del CSS compilado según la versión.
- load_theme(): carga gtk.css con Gtk.CssProvider (tolerante a warnings).
"""
import os
import sys
import argparse

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)


def parse_gtk_args():
    """Parsea --gtk3/--gtk4; si ambos ausentes, intenta GTK 4 y cae a GTK 3."""
    parser = argparse.ArgumentParser(description="Prueba visual de EverforestAdwaita.")
    parser.add_argument("--gtk3", action="store_true", help="Ejecutar con GTK 3")
    parser.add_argument("--gtk4", action="store_true", help="Ejecutar con GTK 4")
    args = parser.parse_args()

    use_gtk3 = args.gtk3
    if not use_gtk3 and not args.gtk4:
        try:
            import gi
            gi.require_version("Gtk", "4.0")
            use_gtk3 = False
        except ValueError:
            use_gtk3 = True
    return use_gtk3


def css_path(use_gtk3):
    """Ruta del gtk.css compilado según la versión."""
    subdir = "gtk-3.0" if use_gtk3 else "gtk-4.0"
    return os.path.join(REPO_ROOT, subdir, "gtk.css")


def load_css(use_gtk3):
    """Carga el tema como provider global. Devuelve el path o lanza SystemExit si no existe."""
    path = css_path(use_gtk3)
    if not os.path.exists(path):
        print(f"Error: No se encontró {path}. Ejecuta 'make compile' primero.")
        sys.exit(1)

    import gi
    if use_gtk3:
        gi.require_version("Gtk", "3.0")
    else:
        gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, Gdk

    provider = Gtk.CssProvider()
    try:
        if use_gtk3:
            provider.load_from_path(path)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
        else:
            provider.load_from_path(path)
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
                )
        print(f"-> CSS de GTK {'3' if use_gtk3 else '4'} cargado desde: {path}")
    except Exception as e:
        print(f"-> Advertencia no crítica al cargar CSS: {e}")
    return provider