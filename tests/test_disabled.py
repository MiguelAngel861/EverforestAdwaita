#!/usr/bin/env python3
"""Test minimalista para diagnosticar switch y checkbox deshabilitados."""
import sys, os, argparse, gi

parser = argparse.ArgumentParser()
parser.add_argument("--gtk3", action="store_true")
parser.add_argument("--gtk4", action="store_true")
args = parser.parse_args()

use_gtk3 = args.gtk3
if not use_gtk3 and not args.gtk4:
    try:
        gi.require_version('Gtk', '4.0')
        use_gtk3 = False
    except ValueError:
        use_gtk3 = True

if use_gtk3:
    print("GTK 3 - Diagnosticando switch y checkbox deshabilitados")
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    Gtk.init([])

    css_provider = Gtk.CssProvider()
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-3.0", "gtk.css")
    if os.path.exists(css_path):
        try:
            css_provider.load_from_path(css_path)
            print(f"-> CSS cargado: {css_path}")
        except Exception as e:
            print(f"-> Error: {e}")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    win = Gtk.Window(title="Diagnóstico Disabled GTK 3")
    win.set_default_size(400, 300)
    win.connect("destroy", Gtk.main_quit)

    vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    vb.set_border_width(15)
    win.add(vb)

    # Switch HABILITADO
    hb1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    hb1.pack_start(Gtk.Label(label="Switch habilitado:"), False, False, 0)
    sw1 = Gtk.Switch()
    sw1.set_active(True)
    hb1.pack_end(sw1, False, False, 0)
    vb.pack_start(hb1, False, False, 0)

    # Switch DESHABILITADO
    hb2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    hb2.pack_start(Gtk.Label(label="Switch deshabilitado:"), False, False, 0)
    sw2 = Gtk.Switch()
    sw2.set_active(True)
    sw2.set_sensitive(False)
    hb2.pack_end(sw2, False, False, 0)
    vb.pack_start(hb2, False, False, 0)

    # Check HABILITADO
    chk1 = Gtk.CheckButton(label="Check habilitado (chequeado)")
    chk1.set_active(True)
    vb.pack_start(chk1, False, False, 0)

    # Check DESHABILITADO
    chk2 = Gtk.CheckButton(label="Check deshabilitado (chequeado)")
    chk2.set_active(True)
    chk2.set_sensitive(False)
    vb.pack_start(chk2, False, False, 0)

    # Entry DESHABILITADA
    ent = Gtk.Entry()
    ent.set_text("Entry deshabilitada")
    ent.set_sensitive(False)
    vb.pack_start(ent, False, False, 0)

    # Radio DESHABILITADO
    r1 = Gtk.RadioButton.new_with_label_from_widget(None, "Radio habilitado")
    r2 = Gtk.RadioButton.new_with_label_from_widget(r1, "Radio deshabilitado")
    r2.set_sensitive(False)
    hb3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    hb3.pack_start(r1, False, False, 0)
    hb3.pack_start(r2, False, False, 0)
    vb.pack_start(hb3, False, False, 0)

    # Info
    lbl = Gtk.Label(label="Verifica: los deshabilitados deben verse apagados\ny no deben responder a clics.")
    lbl.set_xalign(0.0)
    lbl.set_margin_top(10)
    vb.pack_start(lbl, False, False, 0)

    win.show_all()
    Gtk.main()

else:
    print("GTK 4 - Diagnosticando switch y checkbox deshabilitados")
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk, Gdk

    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-4.0", "gtk.css")

    def on_activate(app):
        if os.path.exists(css_path):
            css_provider = Gtk.CssProvider()
            try:
                css_provider.load_from_path(css_path)
                print(f"-> CSS cargado: {css_path}")
            except Exception as e:
                print(f"-> Error: {e}")
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display, css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        win = Gtk.ApplicationWindow(application=app, title="Diagnóstico Disabled GTK 4")
        win.set_default_size(400, 300)

        vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vb.set_margin_top(15)
        vb.set_margin_bottom(15)
        vb.set_margin_start(15)
        vb.set_margin_end(15)
        win.set_child(vb)

        # Switch HABILITADO
        hb1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hb1.append(Gtk.Label(label="Switch habilitado:"))
        sw1 = Gtk.Switch()
        sw1.set_active(True)
        sw1.set_halign(Gtk.Align.END)
        hb1.append(sw1)
        vb.append(hb1)

        # Switch DESHABILITADO
        hb2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hb2.append(Gtk.Label(label="Switch deshabilitado:"))
        sw2 = Gtk.Switch()
        sw2.set_active(True)
        sw2.set_sensitive(False)
        sw2.set_halign(Gtk.Align.END)
        hb2.append(sw2)
        vb.append(hb2)

        # Check HABILITADO
        chk1 = Gtk.CheckButton(label="Check habilitado (chequeado)")
        chk1.set_active(True)
        vb.append(chk1)

        # Check DESHABILITADO
        chk2 = Gtk.CheckButton(label="Check deshabilitado (chequeado)")
        chk2.set_active(True)
        chk2.set_sensitive(False)
        vb.append(chk2)

        # Entry DESHABILITADA
        ent = Gtk.Entry()
        ent.set_text("Entry deshabilitada")
        ent.set_sensitive(False)
        vb.append(ent)

        # Radio DESHABILITADO
        r1 = Gtk.CheckButton(label="Radio habilitado")
        r2 = Gtk.CheckButton(label="Radio deshabilitado")
        r2.set_group(r1)
        r2.set_sensitive(False)
        hb3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hb3.append(r1)
        hb3.append(r2)
        vb.append(hb3)

        # Info
        lbl = Gtk.Label(label="Verifica: los deshabilitados deben verse apagados\ny no deben responder a clics.")
        lbl.set_xalign(0.0)
        lbl.set_margin_top(10)
        vb.append(lbl)

        win.present()

    app = Gtk.Application(application_id="org.everforest.disabled.test")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])
