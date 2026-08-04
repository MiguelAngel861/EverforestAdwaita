#!/usr/bin/env python3
"""Prueba visual rápida: switch, checkbox y botón suggested-action."""
import sys
import gi

sys.path.insert(0, __import__("os").path.dirname(__file__))
import common

use_gtk3 = common.parse_gtk_args()
common.load_css(use_gtk3)

if use_gtk3:
    print("Iniciando prueba visual con GTK 3...")
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    Gtk.init([])

    win = Gtk.Window(title="EverforestAdwaita - Prueba GTK 3")
    win.set_default_size(350, 200)
    win.connect("destroy", Gtk.main_quit)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox.set_margin_top(20)
    vbox.set_margin_bottom(20)
    vbox.set_margin_start(25)
    vbox.set_margin_end(25)
    win.add(vbox)

    hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sw = Gtk.Label(label="Interruptor (GtkSwitch):")
    lbl_sw.set_xalign(0.0)
    sw = Gtk.Switch()
    hbox_sw.pack_start(lbl_sw, True, True, 0)
    hbox_sw.pack_end(sw, False, False, 0)
    vbox.pack_start(hbox_sw, False, False, 0)

    cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
    vbox.pack_start(cb, False, False, 0)

    btn = Gtk.Button(label="Guardar (OK)")
    btn.get_style_context().add_class("suggested-action")
    vbox.pack_start(btn, False, False, 0)

    sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK3) cambiado a: {widget.get_active()}"))

    win.show_all()
    Gtk.main()

else:
    print("Iniciando prueba visual con GTK 4...")
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk

    def on_activate(app):
        win = Gtk.ApplicationWindow(application=app, title="EverforestAdwaita - Prueba GTK 4")
        win.set_default_size(350, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(25)
        vbox.set_margin_end(25)
        win.set_child(vbox)

        hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_sw = Gtk.Label(label="Interruptor (GtkSwitch):")
        lbl_sw.set_xalign(0.0)
        sw = Gtk.Switch()
        sw.set_halign(Gtk.Align.END)

        hbox_sw.append(lbl_sw)
        lbl_sw.set_hexpand(True)
        hbox_sw.append(sw)
        vbox.append(hbox_sw)

        cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
        vbox.append(cb)

        btn = Gtk.Button(label="Guardar (OK)")
        btn.add_css_class("suggested-action")
        vbox.append(btn)

        sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK4) cambiado a: {widget.get_active()}"))

        win.present()

    app = Gtk.Application(application_id="org.everforest.adwaita.visualtest")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])