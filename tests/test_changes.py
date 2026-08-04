#!/usr/bin/env python3
import sys
import os
import argparse
import gi

parser = argparse.ArgumentParser(description="Prueba visual de los componentes cambiados en sesión 9 de EverforestAdwaita.")
parser.add_argument("--gtk3", action="store_true", help="Ejecutar prueba con GTK 3")
parser.add_argument("--gtk4", action="store_true", help="Ejecutar prueba con GTK 4 (predeterminado)")
args = parser.parse_args()

use_gtk3 = args.gtk3
if not use_gtk3 and not args.gtk4:
    try:
        gi.require_version('Gtk', '4.0')
        use_gtk3 = False
    except ValueError:
        use_gtk3 = True

if use_gtk3:
    print("Iniciando visualizador de cambios con GTK 3...")
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk

    Gtk.init([])

    css_provider = Gtk.CssProvider()
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-3.0", "gtk.css")
    if os.path.exists(css_path):
        try:
            css_provider.load_from_path(css_path)
            print(f"-> CSS cargado desde: {css_path}")
        except Exception as e:
            print(f"-> Advertencia al cargar CSS: {e}")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    win = Gtk.Window(title="EverforestAdwaita - Cambios Sesión 9 (GTK 3)")
    win.set_default_size(560, 640)
    win.connect("destroy", Gtk.main_quit)

    hb = Gtk.HeaderBar()
    hb.set_show_close_button(True)
    hb.set_title("Cambios Sesión 9")
    hb.set_subtitle("GTK 3")
    win.set_titlebar(hb)

    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    main_box.set_margin_top(15)
    main_box.set_margin_bottom(15)
    main_box.set_margin_start(15)
    main_box.set_margin_end(15)
    win.add(main_box)

    notebook = Gtk.Notebook()
    main_box.pack_start(notebook, True, True, 0)

    # --- PESTAÑA 1: Vistas y texto (.view / textview) ---
    tab1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    tab1.set_border_width(10)

    lbl1 = Gtk.Label(label="Texto de vistas: #D3C6AA, caret verde #A7C080. Haz clic y escribe.")
    lbl1.set_xalign(0.0)
    tab1.pack_start(lbl1, False, False, 0)

    scrolled_tv = Gtk.ScrolledWindow()
    scrolled_tv.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled_tv.set_min_content_height(110)
    textview = Gtk.TextView()
    textview.set_editable(True)
    textview.set_cursor_visible(True)
    textview.get_buffer().set_text("Este texto vive en un GtkTextView (selector 'textview text').\nLa selección debe verse verde Everforest al enfocar y seleccionar.")
    scrolled_tv.add(textview)
    tab1.pack_start(scrolled_tv, False, False, 0)

    lbl2 = Gtk.Label(label="GtkTreeView (selector .view):")
    lbl2.set_xalign(0.0)
    tab1.pack_start(lbl2, False, False, 0)

    store = Gtk.ListStore(str)
    for i in range(1, 7):
        store.append([f"Fila {i} del árbol - texto .view Everforest"])
    treeview = Gtk.TreeView(model=store)
    treeview.append_column(Gtk.TreeViewColumn("Columnas", Gtk.CellRendererText(), text=0))
    tab1.pack_start(treeview, False, False, 0)

    notebook.append_page(tab1, Gtk.Label(label="Vistas y Texto"))

    # --- PESTAÑA 2: Tooltips y menús legacy ---
    tab2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    tab2.set_border_width(10)

    lbl_tip = Gtk.Label(label="Tooltip: fondo #272E33, borde #374145, texto #D3C6AA.")
    lbl_tip.set_xalign(0.0)
    tab2.pack_start(lbl_tip, False, False, 0)

    btn_tip = Gtk.Button(label="Pasa el cursor por aquí para ver el tooltip Everforest")
    btn_tip.set_tooltip_text("Tooltip Everforest: ya no es negro con texto blanco.")
    tab2.pack_start(btn_tip, False, False, 0)

    lbl_menu = Gtk.Label(label="Menú legacy GTK 3 (fondo #272E33, backdrop #1E2326):")
    lbl_menu.set_xalign(0.0)
    lbl_menu.set_margin_top(10)
    tab2.pack_start(lbl_menu, False, False, 0)

    btn_menu = Gtk.Button(label="Abrir menú contextual legacy")
    menu = Gtk.Menu()
    for i in range(1, 5):
        item = Gtk.MenuItem(label=f"Opción {i} del menú legacy")
        menu.append(item)
    sep = Gtk.SeparatorMenuItem()
    menu.append(sep)
    check_item = Gtk.CheckMenuItem(label="Opción con check (fondo del menú)")
    menu.append(check_item)
    menu.attach_to_widget(btn_menu, None)
    menu.show_all()
    btn_menu.connect("clicked", lambda w: menu.popup_at_widget(
        w, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None))
    tab2.pack_start(btn_menu, False, False, 0)

    notebook.append_page(tab2, Gtk.Label(label="Tooltips y Menús"))

    # --- PESTAÑA 3: Links, estados y barras ---
    tab3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    tab3.set_border_width(10)

    lbl_lnk = Gtk.Label(label="Links: color #7FBBB3 (hover igual, backdrop #9DA9A0).")
    lbl_lnk.set_xalign(0.0)
    tab3.pack_start(lbl_lnk, False, False, 0)

    link = Gtk.LinkButton.new_with_label("https://example.org", "Link Everforest (GtkLinkButton)")
    tab3.pack_start(link, False, False, 0)

    lbl_dark = Gtk.Label(label="")
    lbl_dark.set_markup('<a href="https://example.org">Link con markup (GtkLabel a)</a>')
    lbl_dark.set_xalign(0.0)
    tab3.pack_start(lbl_dark, False, False, 0)

    lbl_dis = Gtk.Label(label="Widgets deshabilitados (grises mapeados grey0/grey1/grey2):")
    lbl_dis.set_xalign(0.0)
    lbl_dis.set_margin_top(10)
    tab3.pack_start(lbl_dis, False, False, 0)

    btn_dis = Gtk.Button(label="Botón deshabilitado")
    btn_dis.set_sensitive(False)
    tab3.pack_start(btn_dis, False, False, 0)

    entry_dis = Gtk.Entry()
    entry_dis.set_text("Entry deshabilitada")
    entry_dis.set_sensitive(False)
    tab3.pack_start(entry_dis, False, False, 0)

    hbox_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    sw_dis = Gtk.Switch()
    sw_dis.set_active(True)
    sw_dis.set_sensitive(False)
    chk_dis = Gtk.CheckButton(label="Check deshabilitado")
    chk_dis.set_active(True)
    chk_dis.set_sensitive(False)
    hbox_dis.pack_start(sw_dis, False, False, 0)
    hbox_dis.pack_start(chk_dis, False, False, 0)
    tab3.pack_start(hbox_dis, False, False, 0)

    lbl_err = Gtk.Label(label="Entries con estado warning/error (mapeados a rojo/ámbar Everforest):")
    lbl_err.set_xalign(0.0)
    lbl_err.set_margin_top(10)
    tab3.pack_start(lbl_err, False, False, 0)

    entry_warn = Gtk.Entry()
    entry_warn.set_text("Entry en estado warning")
    entry_warn.get_style_context().add_class("warning")
    tab3.pack_start(entry_warn, False, False, 0)

    entry_err = Gtk.Entry()
    entry_err.set_text("Entry en estado error")
    entry_err.get_style_context().add_class("error")
    tab3.pack_start(entry_err, False, False, 0)

    lbl_lb = Gtk.Label(label="LevelBar lleno (mapeado a verde #A7C080) y al 45%:")
    lbl_lb.set_xalign(0.0)
    lbl_lb.set_margin_top(10)
    tab3.pack_start(lbl_lb, False, False, 0)

    lb1 = Gtk.LevelBar.new()
    lb1.set_min_value(0)
    lb1.set_max_value(100)
    lb1.add_offset_value("low", 25.0)
    lb1.add_offset_value("high", 75.0)
    lb1.add_offset_value("full", 90.0)
    lb1.set_value(100.0)
    tab3.pack_start(lb1, False, False, 0)

    lb2 = Gtk.LevelBar.new()
    lb2.set_min_value(0)
    lb2.set_max_value(100)
    lb2.add_offset_value("low", 25.0)
    lb2.add_offset_value("high", 75.0)
    lb2.add_offset_value("full", 90.0)
    lb2.set_value(45.0)
    tab3.pack_start(lb2, False, False, 0)

    lbl_pb = Gtk.Label(label="ProgressBar al 66%:")
    lbl_pb.set_xalign(0.0)
    tab3.pack_start(lbl_pb, False, False, 0)

    pb = Gtk.ProgressBar()
    pb.set_fraction(0.66)
    pb.set_text("66%")
    pb.set_show_text(True)
    tab3.pack_start(pb, False, False, 0)

    lbl_info = Gtk.Label(label="InfoBars (fondo #384B55 info / #45443C warning):")
    lbl_info.set_xalign(0.0)
    lbl_info.set_margin_top(10)
    tab3.pack_start(lbl_info, False, False, 0)

    for msg_type in (Gtk.MessageType.INFO, Gtk.MessageType.WARNING):
        ib = Gtk.InfoBar()
        ib.set_message_type(msg_type)
        ib_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        ib_box.pack_start(Gtk.Label(label=f"InfoBar {str(msg_type).split('.')[-1]} - fondos mapeados Everforest"), False, False, 0)
        ib.get_content_area().pack_start(ib_box, True, True, 0)
        ib.show_all()
        tab3.pack_start(ib, False, False, 0)

    notebook.append_page(tab3, Gtk.Label(label="Links y Estados"))

    # --- PESTAÑA 4: Foco y selección (selection:focus mapeado) ---
    tab4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    tab4.set_border_width(10)

    lbl_sel = Gtk.Label(label="Selección enfocada (selection:focus verde, texto #272E33).\nGTK 3 no tiene :focus-within; usa selection:focus (ya mapeado en el base).")
    lbl_sel.set_xalign(0.0)
    tab4.pack_start(lbl_sel, False, False, 0)

    entry_sel = Gtk.Entry()
    entry_sel.set_text("Texto seleccionado dentro de una Entry enfocada")
    entry_sel.connect("realize", lambda w: (w.select_region(0, -1), w.grab_focus()))
    tab4.pack_start(entry_sel, False, False, 0)

    lbl_spin = Gtk.Label(label="SpinButton enfocado:")
    lbl_spin.set_xalign(0.0)
    tab4.pack_start(lbl_spin, False, False, 0)

    spin = Gtk.SpinButton.new_with_range(0, 10, 1)
    spin.set_value(4)
    tab4.pack_start(spin, False, False, 0)

    lbl_focus = Gtk.Label(label="Pulsa Tab para ver el anillo de foco (box-shadow verde #A7C080 en GTK 3):")
    lbl_focus.set_xalign(0.0)
    lbl_focus.set_margin_top(10)
    tab4.pack_start(lbl_focus, False, False, 0)

    btn_focus = Gtk.Button(label="Botón con anillo de foco verde")
    tab4.pack_start(btn_focus, False, False, 0)

    notebook.append_page(tab4, Gtk.Label(label="Foco y Selección"))

    win.show_all()
    Gtk.main()

else:
    print("Iniciando visualizador de cambios con GTK 4...")
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk, Gdk

    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gtk-4.0", "gtk.css")

    def on_activate(app):
        if os.path.exists(css_path):
            css_provider = Gtk.CssProvider()
            try:
                css_provider.load_from_path(css_path)
                print(f"-> CSS cargado desde: {css_path}")
            except Exception as e:
                print(f"-> Advertencia al cargar CSS: {e}")
            display = Gdk.Display.get_default()
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )

        win = Gtk.ApplicationWindow(application=app, title="EverforestAdwaita - Cambios Sesión 9 (GTK 4)")
        win.set_default_size(560, 640)

        hb = Gtk.HeaderBar()
        hb.set_show_title_buttons(True)
        win.set_titlebar(hb)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        win.set_child(main_box)

        notebook = Gtk.Notebook()
        main_box.append(notebook)

        # --- PESTAÑA 1: Vistas y texto (.view / textview) ---
        tab1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        tab1.set_margin_top(10)
        tab1.set_margin_bottom(10)
        tab1.set_margin_start(10)
        tab1.set_margin_end(10)

        lbl1 = Gtk.Label(label="Texto de vistas: #D3C6AA, caret verde #A7C080. Haz clic y escribe.")
        lbl1.set_xalign(0.0)
        tab1.append(lbl1)

        scrolled_tv = Gtk.ScrolledWindow()
        scrolled_tv.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_tv.set_min_content_height(110)
        textview = Gtk.TextView()
        textview.set_editable(True)
        textview.set_cursor_visible(True)
        textview.get_buffer().set_text("Este texto vive en un GtkTextView (selector 'textview text').\nLa selección enfocada debe verse verde Everforest (selection:focus-within).")
        scrolled_tv.set_child(textview)
        tab1.append(scrolled_tv)

        lbl2 = Gtk.Label(label="GtkListView (texto .view):")
        lbl2.set_xalign(0.0)
        tab1.append(lbl2)

        scrolled_lv = Gtk.ScrolledWindow()
        scrolled_lv.set_min_content_height(140)
        model = Gtk.StringList.new([f"Fila {i} de la lista - texto .view Everforest" for i in range(1, 7)])
        factory = Gtk.SignalListItemFactory()

        def on_setup(fact, item):
            item.set_child(Gtk.Label(label="", xalign=0.0))

        def on_bind(fact, item):
            item.get_child().set_text(item.get_item().get_string())

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)
        selection = Gtk.SingleSelection.new(model)
        listview = Gtk.ListView.new(selection, factory)
        scrolled_lv.set_child(listview)
        tab1.append(scrolled_lv)

        notebook.append_page(tab1, Gtk.Label(label="Vistas y Texto"))

        # --- PESTAÑA 2: Tooltips y popover de menú ---
        tab2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        tab2.set_margin_top(10)
        tab2.set_margin_bottom(10)
        tab2.set_margin_start(10)
        tab2.set_margin_end(10)

        lbl_tip = Gtk.Label(label="Tooltip: fondo #272E33, borde #374145, texto #D3C6AA.")
        lbl_tip.set_xalign(0.0)
        tab2.append(lbl_tip)

        btn_tip = Gtk.Button(label="Pasa el cursor por aquí para ver el tooltip Everforest")
        btn_tip.set_tooltip_text("Tooltip Everforest: ya no es negro con texto blanco.")
        tab2.append(btn_tip)

        lbl_menu = Gtk.Label(label="Popover de menú con botón destructivo circular (overrides-gtk4.css):")
        lbl_menu.set_xalign(0.0)
        lbl_menu.set_margin_top(10)
        tab2.append(lbl_menu)

        menubtn = Gtk.MenuButton()
        menubtn.set_label("Menú popover (destructivo circular)")
        popover = Gtk.Popover()
        popover.add_css_class("menu")
        pb_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        pb_box.add_css_class("circular-buttons")

        btn_del = Gtk.Button()
        btn_del.add_css_class("destructive-action")
        btn_del.add_css_class("circular")
        btn_del.add_css_class("image-button")
        btn_del.add_css_class("model")
        btn_del.set_child(Gtk.Image.new_from_icon_name("edit-delete-symbolic"))
        pb_box.append(btn_del)

        btn_norm = Gtk.Button()
        btn_norm.add_css_class("circular")
        btn_norm.add_css_class("image-button")
        btn_norm.set_child(Gtk.Image.new_from_icon_name("list-add-symbolic"))
        pb_box.append(btn_norm)

        popover.set_child(pb_box)
        menubtn.set_popover(popover)
        tab2.append(menubtn)

        notebook.append_page(tab2, Gtk.Label(label="Tooltips y Menús"))

        # --- PESTAÑA 3: Links, estados y barras ---
        tab3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        tab3.set_margin_top(10)
        tab3.set_margin_bottom(10)
        tab3.set_margin_start(10)
        tab3.set_margin_end(10)

        lbl_lnk = Gtk.Label(label="Links: color #7FBBB3 (hover igual, backdrop #9DA9A0).")
        lbl_lnk.set_xalign(0.0)
        tab3.append(lbl_lnk)

        link = Gtk.LinkButton.new("https://example.org")
        link.set_label("Link Everforest (GtkLinkButton)")
        tab3.append(link)

        lbl_dark = Gtk.Label(label="")
        lbl_dark.set_markup('<a href="https://example.org">Link con markup (GtkLabel a)</a>')
        lbl_dark.set_xalign(0.0)
        tab3.append(lbl_dark)

        lbl_dis = Gtk.Label(label="Widgets deshabilitados (grises mapeados grey0/grey1/grey2):")
        lbl_dis.set_xalign(0.0)
        lbl_dis.set_margin_top(10)
        tab3.append(lbl_dis)

        btn_dis = Gtk.Button(label="Botón deshabilitado")
        btn_dis.set_sensitive(False)
        tab3.append(btn_dis)

        entry_dis = Gtk.Entry()
        entry_dis.set_text("Entry deshabilitada")
        entry_dis.set_sensitive(False)
        tab3.append(entry_dis)

        hbox_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        sw_dis = Gtk.Switch()
        sw_dis.set_active(True)
        sw_dis.set_sensitive(False)
        chk_dis = Gtk.CheckButton(label="Check deshabilitado")
        chk_dis.set_active(True)
        chk_dis.set_sensitive(False)
        hbox_dis.append(sw_dis)
        hbox_dis.append(chk_dis)
        tab3.append(hbox_dis)

        lbl_err = Gtk.Label(label="Entries con estado warning/error (mapeados a rojo/ámbar Everforest):")
        lbl_err.set_xalign(0.0)
        lbl_err.set_margin_top(10)
        tab3.append(lbl_err)

        entry_warn = Gtk.Entry()
        entry_warn.set_text("Entry en estado warning")
        entry_warn.add_css_class("warning")
        tab3.append(entry_warn)

        entry_err = Gtk.Entry()
        entry_err.set_text("Entry en estado error")
        entry_err.add_css_class("error")
        tab3.append(entry_err)

        lbl_lb = Gtk.Label(label="LevelBar lleno (mapeado a verde #A7C080) y al 45%:")
        lbl_lb.set_xalign(0.0)
        lbl_lb.set_margin_top(10)
        tab3.append(lbl_lb)

        lb1 = Gtk.LevelBar.new()
        lb1.set_min_value(0)
        lb1.set_max_value(100)
        lb1.add_offset_value("low", 25.0)
        lb1.add_offset_value("high", 75.0)
        lb1.add_offset_value("full", 90.0)
        lb1.set_value(100.0)
        tab3.append(lb1)

        lb2 = Gtk.LevelBar.new()
        lb2.set_min_value(0)
        lb2.set_max_value(100)
        lb2.add_offset_value("low", 25.0)
        lb2.add_offset_value("high", 75.0)
        lb2.add_offset_value("full", 90.0)
        lb2.set_value(45.0)
        tab3.append(lb2)

        lbl_pb = Gtk.Label(label="ProgressBar al 66%:")
        lbl_pb.set_xalign(0.0)
        tab3.append(lbl_pb)

        pb = Gtk.ProgressBar()
        pb.set_fraction(0.66)
        pb.set_text("66%")
        pb.set_show_text(True)
        tab3.append(pb)

        lbl_info = Gtk.Label(label="InfoBars (fondo #384B55 info / #45443C warning):")
        lbl_info.set_xalign(0.0)
        lbl_info.set_margin_top(10)
        tab3.append(lbl_info)

        for msg_type in (Gtk.MessageType.INFO, Gtk.MessageType.WARNING):
            ib = Gtk.InfoBar()
            ib.set_message_type(msg_type)
            ib.add_child(Gtk.Label(label=f"InfoBar {str(msg_type).split('.')[-1]} - fondos mapeados Everforest"))
            ib.set_revealed(True)
            tab3.append(ib)

        notebook.append_page(tab3, Gtk.Label(label="Links y Estados"))

        # --- PESTAÑA 4: Foco y selección (overrides-gtk4.css) ---
        tab4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        tab4.set_margin_top(10)
        tab4.set_margin_bottom(10)
        tab4.set_margin_start(10)
        tab4.set_margin_end(10)

        lbl_sel = Gtk.Label(label="Selección enfocada (selection:focus-within verde, texto #272E33,\nregla GTK4-only de overrides-gtk4.css):")
        lbl_sel.set_xalign(0.0)
        tab4.append(lbl_sel)

        entry_sel = Gtk.Entry()
        entry_sel.set_text("Texto seleccionado dentro de una Entry enfocada")
        entry_sel.connect("realize", lambda w: (w.select_region(0, -1), w.grab_focus()))
        tab4.append(entry_sel)

        lbl_tv = Gtk.Label(label="Selección en TextView:")
        lbl_tv.set_xalign(0.0)
        lbl_tv.set_margin_top(8)
        tab4.append(lbl_tv)

        scrolled_sel = Gtk.ScrolledWindow()
        scrolled_sel.set_min_content_height(80)
        tv_sel = Gtk.TextView()
        buf_sel = tv_sel.get_buffer()
        buf_sel.set_text("Párrafo con selección enfocada (textview > text > selection:focus-within)")
        tv_sel.set_editable(True)
        tv_sel.set_cursor_visible(True)
        start = buf_sel.get_start_iter()
        end = buf_sel.get_end_iter()
        buf_sel.select_range(start, end)
        tv_sel.connect("realize", lambda w: w.grab_focus())
        scrolled_sel.set_child(tv_sel)
        tab4.append(scrolled_sel)

        lbl_focus = Gtk.Label(label="Pulsa Tab para ver el anillo de foco verde (focus-visible, overrides-gtk4.css):")
        lbl_focus.set_xalign(0.0)
        lbl_focus.set_margin_top(10)
        tab4.append(lbl_focus)

        btn_focus = Gtk.Button(label="Botón con anillo de foco verde (outline rgba(167,192,128,0.7))")
        tab4.append(btn_focus)

        dropdown = Gtk.DropDown.new_from_strings(["Opción de dropdown 1", "Opción de dropdown 2"])
        dropdown.set_selected(0)
        tab4.append(dropdown)

        notebook.append_page(tab4, Gtk.Label(label="Foco y Selección"))

        win.present()

    app = Gtk.Application(application_id="org.everforest.adwaita.changestest")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])
