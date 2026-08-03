#!/usr/bin/env python3
import sys
import os
import argparse
import gi

# Configurar argumentos de línea de comandos para seleccionar la versión de GTK
parser = argparse.ArgumentParser(description="Herramienta de prueba visual para widgets de EverforestAdwaita.")
parser.add_argument("--gtk3", action="store_true", help="Ejecutar prueba con GTK 3")
parser.add_argument("--gtk4", action="store_true", help="Ejecutar prueba con GTK 4 (predeterminado)")
args = parser.parse_args()

use_gtk3 = args.gtk3
if not use_gtk3 and not args.gtk4:
    # Por defecto intenta usar GTK 4, si falla cae a GTK 3
    try:
        gi.require_version('Gtk', '4.0')
        use_gtk3 = False
    except ValueError:
        use_gtk3 = True

if use_gtk3:
    print("Iniciando prueba visual con GTK 3...")
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    
    Gtk.init([])
    
    # Cargar archivo CSS compilado de GTK 3
    css_provider = Gtk.CssProvider()
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-3.0", "gtk.css")
    if os.path.exists(css_path):
        try:
            css_provider.load_from_path(css_path)
            print(f"-> CSS de GTK 3 cargado desde: {css_path}")
        except Exception as e:
            print(f"-> Advertencia no crítica al cargar CSS en GTK 3: {e}")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    else:
        print(f"Error: No se encontró el CSS compilado en {css_path}. Ejecuta 'make compile' primero.")
        sys.exit(1)

    # Crear ventana de GTK 3
    win = Gtk.Window(title="EverforestAdwaita - Prueba GTK 3")
    win.set_default_size(350, 200)
    win.connect("destroy", Gtk.main_quit)
    
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox.set_margin_top(20)
    vbox.set_margin_bottom(20)
    vbox.set_margin_start(25)
    vbox.set_margin_end(25)
    win.add(vbox)
    
    # Switch
    hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sw = Gtk.Label(label="Interruptor (GtkSwitch):")
    lbl_sw.set_xalign(0.0)
    sw = Gtk.Switch()
    hbox_sw.pack_start(lbl_sw, True, True, 0)
    hbox_sw.pack_end(sw, False, False, 0)
    vbox.pack_start(hbox_sw, False, False, 0)
    
    # Checkbox
    cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
    vbox.pack_start(cb, False, False, 0)
    
    # Button suggested action (OK)
    btn = Gtk.Button(label="Guardar (OK)")
    btn.get_style_context().add_class("suggested-action")
    vbox.pack_start(btn, False, False, 0)
    
    # Imprimir estado del switch en terminal al cambiar
    sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK3) cambiado a: {widget.get_active()}"))
    
    win.show_all()
    Gtk.main()

else:
    print("Iniciando prueba visual con GTK 4...")
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk, Gdk
    
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-4.0", "gtk.css")
    
    def on_activate(app):
        # Cargar archivo CSS compilado de GTK 4
        if os.path.exists(css_path):
            css_provider = Gtk.CssProvider()
            try:
                css_provider.load_from_path(css_path)
                print(f"-> CSS de GTK 4 cargado desde: {css_path}")
            except Exception as e:
                print(f"-> Advertencia no crítica al cargar CSS en GTK 4: {e}")
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
        else:
            print(f"Error: No se encontró el CSS compilado en {css_path}. Ejecuta 'make compile' primero.")
            sys.exit(1)

        win = Gtk.ApplicationWindow(application=app, title="EverforestAdwaita - Prueba GTK 4")
        win.set_default_size(350, 200)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(25)
        vbox.set_margin_end(25)
        win.set_child(vbox)
        
        # Switch
        hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_sw = Gtk.Label(label="Interruptor (GtkSwitch):")
        lbl_sw.set_xalign(0.0)
        sw = Gtk.Switch()
        sw.set_halign(Gtk.Align.END)
        
        hbox_sw.append(lbl_sw)
        # Forzar que el label tome todo el espacio posible para empujar el switch a la derecha
        lbl_sw.set_hexpand(True)
        hbox_sw.append(sw)
        vbox.append(hbox_sw)
        
        # Checkbox
        cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
        vbox.append(cb)
        
        # Button suggested action (OK)
        btn = Gtk.Button(label="Guardar (OK)")
        btn.add_css_class("suggested-action")
        vbox.append(btn)
        
        # Imprimir estado del switch en terminal al cambiar
        sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK4) cambiado a: {widget.get_active()}"))
        
        win.present()

    app = Gtk.Application(application_id="org.everforest.adwaita.visualtest")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])
