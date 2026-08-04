#!/usr/bin/env python3
"""Prueba visual unificada de EverforestAdwaita (GTK 3 / GTK 4).

Cubre en 6 pestañas todos los widgets y estados del tema:
  1. Flotantes y Sombras: tooltip, popover, dropdown, radios, diálogo modal.
  2. Controles y Listas: botones semánticos, entry, switch, check, ListBox.
  3. Vistas y Texto: TextView, TreeView (GTK3) / ListView (GTK4).
  4. Tooltips y Menús: tooltip, menú legacy (GTK3) / popover de menú (GTK4).
  5. Links, Estados y Barras: links, deshabilitados, warning/error, LevelBar, ProgressBar, InfoBars.
  6. Foco y Selección: selección enfocada, SpinButton, anillo de foco, DropDown (GTK4).

Uso: python3 tests/test_visual.py [--gtk3|--gtk4]
"""
import sys
import os
import gi

sys.path.insert(0, os.path.dirname(__file__))
import common

use_gtk3 = common.parse_gtk_args()
common.load_css(use_gtk3)

if use_gtk3:
    print("Iniciando prueba visual unificada con GTK 3...")
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk

    Gtk.init([])

    win = Gtk.Window(title="EverforestAdwaita - Prueba Visual (GTK 3)")
    win.set_default_size(600, 680)
    win.connect("destroy", Gtk.main_quit)

    hb = Gtk.HeaderBar()
    hb.set_show_close_button(True)
    hb.set_title("EverforestAdwaita")
    hb.set_subtitle("Prueba visual unificada GTK 3")
    win.set_titlebar(hb)

    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    main_box.set_margin_top(12)
    main_box.set_margin_bottom(12)
    main_box.set_margin_start(12)
    main_box.set_margin_end(12)
    win.add(main_box)

    notebook = Gtk.Notebook()
    main_box.pack_start(notebook, True, True, 0)

    def new_tab():
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(10)
        return box

    # --- PESTAÑA 1: Flotantes y Sombras ---
    tab1 = new_tab()

    btn_tooltip = Gtk.Button(label="Pasa el cursor aquí (Tooltip - Nivel 1)")
    btn_tooltip.set_tooltip_text("Este tooltip de información usa una sombra discreta de Nivel 1.")
    tab1.pack_start(btn_tooltip, False, False, 0)

    btn_popover = Gtk.Button(label="Mostrar Popover (Nivel 2)")
    popover = Gtk.Popover()
    popover.set_relative_to(btn_popover)
    popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    popover_content.set_border_width(10)
    popover_content.pack_start(Gtk.Label(label="Menú / Popover Flotante"), False, False, 0)
    pop_btn1 = Gtk.ModelButton(label="Opción 1")
    pop_btn2 = Gtk.ModelButton(label="Opción 2")
    popover_content.pack_start(pop_btn1, False, False, 0)
    popover_content.pack_start(pop_btn2, False, False, 0)
    popover.add(popover_content)
    btn_popover.connect("clicked", lambda w: popover.popup() if not popover.get_visible() else popover.popdown())
    tab1.pack_start(btn_popover, False, False, 0)

    combo_box = Gtk.ComboBoxText()
    combo_box.append_text("Opción de Dropdown 1 (Nivel 2)")
    combo_box.append_text("Opción de Dropdown 2 (Nivel 2)")
    combo_box.append_text("Opción de Dropdown 3 (Nivel 2)")
    combo_box.set_active(0)
    tab1.pack_start(combo_box, False, False, 0)

    hbox_radio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
    lbl_radio = Gtk.Label(label="Selección Única (Radios Cuadrados):")
    lbl_radio.set_xalign(0.0)
    radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Opción A")
    radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Opción B")
    hbox_radio.pack_start(lbl_radio, True, True, 0)
    hbox_radio.pack_end(radio1, False, False, 0)
    hbox_radio.pack_end(radio2, False, False, 0)
    tab1.pack_start(hbox_radio, False, False, 0)

    def on_show_dialog(btn):
        dialog = Gtk.MessageDialog(
            transient_for=win,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Ventana de Diálogo (Sombra Nivel 3)",
            secondary_text="Esta ventana modal demuestra la elevación de nivel 3 con bordes rectos y sombras suaves."
        )
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show_all()

    btn_dialog = Gtk.Button(label="Lanzar Diálogo Modal (Nivel 3)")
    btn_dialog.connect("clicked", on_show_dialog)
    tab1.pack_start(btn_dialog, False, False, 0)

    notebook.append_page(tab1, Gtk.Label(label="Flotantes y Sombras"))

    # --- PESTAÑA 2: Controles y Listas ---
    tab2 = new_tab()

    btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btn_suggested = Gtk.Button(label="Sugerido")
    btn_suggested.get_style_context().add_class("suggested-action")
    btn_destructive = Gtk.Button(label="Destructivo")
    btn_destructive.get_style_context().add_class("destructive-action")
    btn_flat = Gtk.Button(label="Plano")
    btn_flat.get_style_context().add_class("flat")
    btn_box.pack_start(btn_suggested, True, True, 0)
    btn_box.pack_start(btn_destructive, True, True, 0)
    btn_box.pack_start(btn_flat, True, True, 0)
    tab2.pack_start(btn_box, False, False, 0)

    entry = Gtk.Entry()
    entry.set_placeholder_text("Escribe aquí... (Input en Foco)")
    tab2.pack_start(entry, False, False, 0)

    hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sw = Gtk.Label(label="Interruptor Everforest:")
    lbl_sw.set_xalign(0.0)
    sw = Gtk.Switch()
    hbox_sw.pack_start(lbl_sw, True, True, 0)
    hbox_sw.pack_end(sw, False, False, 0)
    tab2.pack_start(hbox_sw, False, False, 0)
    sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK3) cambiado a: {widget.get_active()}"))

    cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
    tab2.pack_start(cb, False, False, 0)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled.set_min_content_height(150)
    listbox = Gtk.ListBox()
    for i in range(1, 15):
        row = Gtk.ListBoxRow()
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row_box.set_margin_top(5)
        row_box.set_margin_bottom(5)
        row_box.set_margin_start(10)
        row_box.pack_start(Gtk.Label(label=f"Fila {i} - Elemento de Lista Seleccionable"), False, False, 0)
        row.add(row_box)
        listbox.add(row)
    scrolled.add(listbox)
    tab2.pack_start(scrolled, True, True, 0)

    notebook.append_page(tab2, Gtk.Label(label="Controles y Listas"))

    # --- PESTAÑA 3: Vistas y Texto ---
    tab3 = new_tab()

    lbl1 = Gtk.Label(label="Texto de vistas: #D3C6AA, caret verde #A7C080. Haz clic y escribe.")
    lbl1.set_xalign(0.0)
    tab3.pack_start(lbl1, False, False, 0)

    scrolled_tv = Gtk.ScrolledWindow()
    scrolled_tv.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled_tv.set_min_content_height(110)
    textview = Gtk.TextView()
    textview.set_editable(True)
    textview.set_cursor_visible(True)
    textview.get_buffer().set_text("Este texto vive en un GtkTextView (selector 'textview text').\nLa selección debe verse verde Everforest al enfocar y seleccionar.")
    scrolled_tv.add(textview)
    tab3.pack_start(scrolled_tv, False, False, 0)

    lbl2 = Gtk.Label(label="GtkTreeView (selector .view):")
    lbl2.set_xalign(0.0)
    tab3.pack_start(lbl2, False, False, 0)

    store = Gtk.ListStore(str)
    for i in range(1, 7):
        store.append([f"Fila {i} del árbol - texto .view Everforest"])
    treeview = Gtk.TreeView(model=store)
    treeview.append_column(Gtk.TreeViewColumn("Columnas", Gtk.CellRendererText(), text=0))
    tab3.pack_start(treeview, False, False, 0)

    notebook.append_page(tab3, Gtk.Label(label="Vistas y Texto"))

    # --- PESTAÑA 4: Tooltips y Menús ---
    tab4 = new_tab()

    lbl_tip = Gtk.Label(label="Tooltip: fondo #272E33, borde #374145, texto #D3C6AA.")
    lbl_tip.set_xalign(0.0)
    tab4.pack_start(lbl_tip, False, False, 0)

    btn_tip = Gtk.Button(label="Pasa el cursor por aquí para ver el tooltip Everforest")
    btn_tip.set_tooltip_text("Tooltip Everforest: ya no es negro con texto blanco.")
    tab4.pack_start(btn_tip, False, False, 0)

    lbl_menu = Gtk.Label(label="Menú legacy GTK 3 (fondo #272E33, backdrop #1E2326):")
    lbl_menu.set_xalign(0.0)
    lbl_menu.set_margin_top(10)
    tab4.pack_start(lbl_menu, False, False, 0)

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
    tab4.pack_start(btn_menu, False, False, 0)

    notebook.append_page(tab4, Gtk.Label(label="Tooltips y Menús"))

    # --- PESTAÑA 5: Links, Estados y Barras ---
    tab5 = new_tab()

    lbl_lnk = Gtk.Label(label="Links: color #7FBBB3 (hover igual, backdrop #9DA9A0).")
    lbl_lnk.set_xalign(0.0)
    tab5.pack_start(lbl_lnk, False, False, 0)

    link = Gtk.LinkButton.new_with_label("https://example.org", "Link Everforest (GtkLinkButton)")
    tab5.pack_start(link, False, False, 0)

    lbl_dark = Gtk.Label(label="")
    lbl_dark.set_markup('<a href="https://example.org">Link con markup (GtkLabel a)</a>')
    lbl_dark.set_xalign(0.0)
    tab5.pack_start(lbl_dark, False, False, 0)

    lbl_dis = Gtk.Label(label="Habilitados vs deshabilitados (grises mapeados grey0/grey1/grey2):")
    lbl_dis.set_xalign(0.0)
    lbl_dis.set_margin_top(10)
    tab5.pack_start(lbl_dis, False, False, 0)

    hbox_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    btn_ok = Gtk.Button(label="Botón habilitado")
    btn_dis = Gtk.Button(label="Botón deshabilitado")
    btn_dis.set_sensitive(False)
    hbox_btns.pack_start(btn_ok, True, True, 0)
    hbox_btns.pack_start(btn_dis, True, True, 0)
    tab5.pack_start(hbox_btns, False, False, 0)

    entry_dis = Gtk.Entry()
    entry_dis.set_text("Entry deshabilitada")
    entry_dis.set_sensitive(False)
    tab5.pack_start(entry_dis, False, False, 0)

    hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    hbox_sw.pack_start(Gtk.Label(label="Switch habilitado:"), False, False, 0)
    sw1 = Gtk.Switch()
    sw1.set_active(True)
    hbox_sw.pack_end(sw1, False, False, 0)
    tab5.pack_start(hbox_sw, False, False, 0)

    hbox_sw_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    hbox_sw_dis.pack_start(Gtk.Label(label="Switch deshabilitado:"), False, False, 0)
    sw2 = Gtk.Switch()
    sw2.set_active(True)
    sw2.set_sensitive(False)
    hbox_sw_dis.pack_end(sw2, False, False, 0)
    tab5.pack_start(hbox_sw_dis, False, False, 0)

    chk_ok = Gtk.CheckButton(label="Check habilitado (chequeado)")
    chk_ok.set_active(True)
    tab5.pack_start(chk_ok, False, False, 0)

    chk_dis = Gtk.CheckButton(label="Check deshabilitado (chequeado)")
    chk_dis.set_active(True)
    chk_dis.set_sensitive(False)
    tab5.pack_start(chk_dis, False, False, 0)

    r1 = Gtk.RadioButton.new_with_label_from_widget(None, "Radio habilitado")
    r2 = Gtk.RadioButton.new_with_label_from_widget(r1, "Radio deshabilitado")
    r2.set_sensitive(False)
    hbox_radio_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    hbox_radio_dis.pack_start(r1, False, False, 0)
    hbox_radio_dis.pack_start(r2, False, False, 0)
    tab5.pack_start(hbox_radio_dis, False, False, 0)

    lbl_err = Gtk.Label(label="Entries con estado warning/error (mapeados a rojo/ámbar Everforest):")
    lbl_err.set_xalign(0.0)
    lbl_err.set_margin_top(10)
    tab5.pack_start(lbl_err, False, False, 0)

    entry_warn = Gtk.Entry()
    entry_warn.set_text("Entry en estado warning")
    entry_warn.get_style_context().add_class("warning")
    tab5.pack_start(entry_warn, False, False, 0)

    entry_err = Gtk.Entry()
    entry_err.set_text("Entry en estado error")
    entry_err.get_style_context().add_class("error")
    tab5.pack_start(entry_err, False, False, 0)

    lbl_lb = Gtk.Label(label="LevelBar lleno (mapeado a verde #A7C080) y al 45%:")
    lbl_lb.set_xalign(0.0)
    lbl_lb.set_margin_top(10)
    tab5.pack_start(lbl_lb, False, False, 0)

    lb1 = Gtk.LevelBar.new()
    lb1.set_min_value(0)
    lb1.set_max_value(100)
    lb1.add_offset_value("low", 25.0)
    lb1.add_offset_value("high", 75.0)
    lb1.add_offset_value("full", 90.0)
    lb1.set_value(100.0)
    tab5.pack_start(lb1, False, False, 0)

    lb2 = Gtk.LevelBar.new()
    lb2.set_min_value(0)
    lb2.set_max_value(100)
    lb2.add_offset_value("low", 25.0)
    lb2.add_offset_value("high", 75.0)
    lb2.add_offset_value("full", 90.0)
    lb2.set_value(45.0)
    tab5.pack_start(lb2, False, False, 0)

    lbl_pb = Gtk.Label(label="ProgressBar al 66%:")
    lbl_pb.set_xalign(0.0)
    tab5.pack_start(lbl_pb, False, False, 0)

    pb = Gtk.ProgressBar()
    pb.set_fraction(0.66)
    pb.set_text("66%")
    pb.set_show_text(True)
    tab5.pack_start(pb, False, False, 0)

    lbl_info = Gtk.Label(label="InfoBars (fondo #384B55 info / #45443C warning):")
    lbl_info.set_xalign(0.0)
    lbl_info.set_margin_top(10)
    tab5.pack_start(lbl_info, False, False, 0)

    for msg_type in (Gtk.MessageType.INFO, Gtk.MessageType.WARNING):
        ib = Gtk.InfoBar()
        ib.set_message_type(msg_type)
        ib_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        ib_box.pack_start(Gtk.Label(label=f"InfoBar {str(msg_type).split('.')[-1]} - fondos mapeados Everforest"), False, False, 0)
        ib.get_content_area().pack_start(ib_box, True, True, 0)
        ib.show_all()
        tab5.pack_start(ib, False, False, 0)

    notebook.append_page(tab5, Gtk.Label(label="Links y Estados"))

    # --- PESTAÑA 6: Foco y Selección ---
    tab6 = new_tab()

    lbl_sel = Gtk.Label(label="Selección enfocada (selection:focus verde, texto #272E33).\nGTK 3 no tiene :focus-within; usa selection:focus (ya mapeado en el base).")
    lbl_sel.set_xalign(0.0)
    tab6.pack_start(lbl_sel, False, False, 0)

    entry_sel = Gtk.Entry()
    entry_sel.set_text("Texto seleccionado dentro de una Entry enfocada")
    entry_sel.connect("realize", lambda w: (w.select_region(0, -1), w.grab_focus()))
    tab6.pack_start(entry_sel, False, False, 0)

    lbl_spin = Gtk.Label(label="SpinButton enfocado:")
    lbl_spin.set_xalign(0.0)
    tab6.pack_start(lbl_spin, False, False, 0)

    spin = Gtk.SpinButton.new_with_range(0, 10, 1)
    spin.set_value(4)
    tab6.pack_start(spin, False, False, 0)

    lbl_focus = Gtk.Label(label="Pulsa Tab para ver el anillo de foco (box-shadow verde #A7C080 en GTK 3):")
    lbl_focus.set_xalign(0.0)
    lbl_focus.set_margin_top(10)
    tab6.pack_start(lbl_focus, False, False, 0)

    btn_focus = Gtk.Button(label="Botón con anillo de foco verde")
    tab6.pack_start(btn_focus, False, False, 0)

    notebook.append_page(tab6, Gtk.Label(label="Foco y Selección"))

    win.show_all()
    Gtk.main()

else:
    print("Iniciando prueba visual unificada con GTK 4...")
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk

    def on_activate(app):
        win = Gtk.ApplicationWindow(application=app, title="EverforestAdwaita - Prueba Visual (GTK 4)")
        win.set_default_size(600, 680)

        hb = Gtk.HeaderBar()
        hb.set_show_title_buttons(True)
        win.set_titlebar(hb)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        win.set_child(main_box)

        notebook = Gtk.Notebook()
        main_box.append(notebook)

        def new_tab():
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            box.set_margin_top(10)
            box.set_margin_bottom(10)
            box.set_margin_start(10)
            box.set_margin_end(10)
            return box

        # --- PESTAÑA 1: Flotantes y Sombras ---
        tab1 = new_tab()

        btn_tooltip = Gtk.Button(label="Pasa el cursor aquí (Tooltip - Nivel 1)")
        btn_tooltip.set_tooltip_text("Este tooltip de información usa una sombra discreta de Nivel 1.")
        tab1.append(btn_tooltip)

        btn_popover = Gtk.Button(label="Mostrar Popover (Nivel 2)")
        popover = Gtk.Popover()
        popover.set_parent(btn_popover)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        popover_content.set_margin_top(10)
        popover_content.set_margin_bottom(10)
        popover_content.set_margin_start(10)
        popover_content.set_margin_end(10)
        popover_content.append(Gtk.Label(label="Menú / Popover Flotante"))
        pop_btn1 = Gtk.Button(label="Opción 1")
        pop_btn1.add_css_class("flat")
        pop_btn2 = Gtk.Button(label="Opción 2")
        pop_btn2.add_css_class("flat")
        popover_content.append(pop_btn1)
        popover_content.append(pop_btn2)
        popover.set_child(popover_content)
        btn_popover.connect("clicked", lambda w: popover.popup() if not popover.get_visible() else popover.popdown())
        tab1.append(btn_popover)

        combo_box = Gtk.ComboBoxText()
        combo_box.append_text("Opción de Dropdown 1 (Nivel 2)")
        combo_box.append_text("Opción de Dropdown 2 (Nivel 2)")
        combo_box.append_text("Opción de Dropdown 3 (Nivel 2)")
        combo_box.set_active(0)
        tab1.append(combo_box)

        hbox_radio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        lbl_radio = Gtk.Label(label="Selección Única (Radios Cuadrados):")
        lbl_radio.set_xalign(0.0)
        radio1 = Gtk.CheckButton(label="Opción A")
        radio2 = Gtk.CheckButton(label="Opción B")
        radio2.set_group(radio1)
        hbox_radio.append(lbl_radio)
        lbl_radio.set_hexpand(True)
        hbox_radio.append(radio1)
        hbox_radio.append(radio2)
        tab1.append(hbox_radio)

        def on_show_dialog(btn):
            dialog = Gtk.MessageDialog(
                transient_for=win,
                modal=True,
                destroy_with_parent=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Ventana de Diálogo (Sombra Nivel 3)",
                secondary_text="Esta ventana modal demuestra la elevación de nivel 3 con bordes rectos y sombras suaves."
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.present()

        btn_dialog = Gtk.Button(label="Lanzar Diálogo Modal (Nivel 3)")
        btn_dialog.connect("clicked", on_show_dialog)
        tab1.append(btn_dialog)

        notebook.append_page(tab1, Gtk.Label(label="Flotantes y Sombras"))

        # --- PESTAÑA 2: Controles y Listas ---
        tab2 = new_tab()

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_suggested = Gtk.Button(label="Sugerido")
        btn_suggested.add_css_class("suggested-action")
        btn_destructive = Gtk.Button(label="Destructivo")
        btn_destructive.add_css_class("destructive-action")
        btn_flat = Gtk.Button(label="Plano")
        btn_flat.add_css_class("flat")
        btn_box.append(btn_suggested)
        btn_suggested.set_hexpand(True)
        btn_box.append(btn_destructive)
        btn_destructive.set_hexpand(True)
        btn_box.append(btn_flat)
        btn_flat.set_hexpand(True)
        tab2.append(btn_box)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Escribe aquí... (Input en Foco)")
        tab2.append(entry)

        hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_sw = Gtk.Label(label="Interruptor Everforest:")
        lbl_sw.set_xalign(0.0)
        sw = Gtk.Switch()
        sw.set_halign(Gtk.Align.END)
        hbox_sw.append(lbl_sw)
        lbl_sw.set_hexpand(True)
        hbox_sw.append(sw)
        tab2.append(hbox_sw)
        sw.connect("notify::active", lambda widget, pspec: print(f"Switch (GTK4) cambiado a: {widget.get_active()}"))

        cb = Gtk.CheckButton(label="Casilla de verificación (GtkCheckButton)")
        tab2.append(cb)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(150)
        scrolled.set_vexpand(True)
        listbox = Gtk.ListBox()
        for i in range(1, 15):
            row = Gtk.ListBoxRow()
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            row_box.set_margin_top(5)
            row_box.set_margin_bottom(5)
            row_box.set_margin_start(10)
            row_box.append(Gtk.Label(label=f"Fila {i} - Elemento de Lista Seleccionable"))
            row.set_child(row_box)
            listbox.append(row)
        scrolled.set_child(listbox)
        tab2.append(scrolled)

        notebook.append_page(tab2, Gtk.Label(label="Controles y Listas"))

        # --- PESTAÑA 3: Vistas y Texto ---
        tab3 = new_tab()

        lbl1 = Gtk.Label(label="Texto de vistas: #D3C6AA, caret verde #A7C080. Haz clic y escribe.")
        lbl1.set_xalign(0.0)
        tab3.append(lbl1)

        scrolled_tv = Gtk.ScrolledWindow()
        scrolled_tv.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_tv.set_min_content_height(110)
        textview = Gtk.TextView()
        textview.set_editable(True)
        textview.set_cursor_visible(True)
        textview.get_buffer().set_text("Este texto vive en un GtkTextView (selector 'textview text').\nLa selección enfocada debe verse verde Everforest (selection:focus-within).")
        scrolled_tv.set_child(textview)
        tab3.append(scrolled_tv)

        lbl2 = Gtk.Label(label="GtkListView (texto .view):")
        lbl2.set_xalign(0.0)
        tab3.append(lbl2)

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
        tab3.append(scrolled_lv)

        notebook.append_page(tab3, Gtk.Label(label="Vistas y Texto"))

        # --- PESTAÑA 4: Tooltips y Menús ---
        tab4 = new_tab()

        lbl_tip = Gtk.Label(label="Tooltip: fondo #272E33, borde #374145, texto #D3C6AA.")
        lbl_tip.set_xalign(0.0)
        tab4.append(lbl_tip)

        btn_tip = Gtk.Button(label="Pasa el cursor por aquí para ver el tooltip Everforest")
        btn_tip.set_tooltip_text("Tooltip Everforest: ya no es negro con texto blanco.")
        tab4.append(btn_tip)

        lbl_menu = Gtk.Label(label="Popover de menú con botón destructivo circular (overrides-gtk4.css):")
        lbl_menu.set_xalign(0.0)
        lbl_menu.set_margin_top(10)
        tab4.append(lbl_menu)

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
        tab4.append(menubtn)

        notebook.append_page(tab4, Gtk.Label(label="Tooltips y Menús"))

        # --- PESTAÑA 5: Links, Estados y Barras ---
        tab5 = new_tab()

        lbl_lnk = Gtk.Label(label="Links: color #7FBBB3 (hover igual, backdrop #9DA9A0).")
        lbl_lnk.set_xalign(0.0)
        tab5.append(lbl_lnk)

        link = Gtk.LinkButton.new("https://example.org")
        link.set_label("Link Everforest (GtkLinkButton)")
        tab5.append(link)

        lbl_dark = Gtk.Label(label="")
        lbl_dark.set_markup('<a href="https://example.org">Link con markup (GtkLabel a)</a>')
        lbl_dark.set_xalign(0.0)
        tab5.append(lbl_dark)

        lbl_dis = Gtk.Label(label="Habilitados vs deshabilitados (grises mapeados grey0/grey1/grey2):")
        lbl_dis.set_xalign(0.0)
        lbl_dis.set_margin_top(10)
        tab5.append(lbl_dis)

        hbox_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_ok = Gtk.Button(label="Botón habilitado")
        btn_dis = Gtk.Button(label="Botón deshabilitado")
        btn_dis.set_sensitive(False)
        hbox_btns.append(btn_ok)
        btn_ok.set_hexpand(True)
        hbox_btns.append(btn_dis)
        btn_dis.set_hexpand(True)
        tab5.append(hbox_btns)

        entry_dis = Gtk.Entry()
        entry_dis.set_text("Entry deshabilitada")
        entry_dis.set_sensitive(False)
        tab5.append(entry_dis)

        hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hbox_sw.append(Gtk.Label(label="Switch habilitado:"))
        sw1 = Gtk.Switch()
        sw1.set_active(True)
        sw1.set_halign(Gtk.Align.END)
        hbox_sw.append(sw1)
        tab5.append(hbox_sw)

        hbox_sw_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hbox_sw_dis.append(Gtk.Label(label="Switch deshabilitado:"))
        sw2 = Gtk.Switch()
        sw2.set_active(True)
        sw2.set_sensitive(False)
        sw2.set_halign(Gtk.Align.END)
        hbox_sw_dis.append(sw2)
        tab5.append(hbox_sw_dis)

        chk_ok = Gtk.CheckButton(label="Check habilitado (chequeado)")
        chk_ok.set_active(True)
        tab5.append(chk_ok)

        chk_dis = Gtk.CheckButton(label="Check deshabilitado (chequeado)")
        chk_dis.set_active(True)
        chk_dis.set_sensitive(False)
        tab5.append(chk_dis)

        r1 = Gtk.CheckButton(label="Radio habilitado")
        r2 = Gtk.CheckButton(label="Radio deshabilitado")
        r2.set_group(r1)
        r2.set_sensitive(False)
        hbox_radio_dis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox_radio_dis.append(r1)
        hbox_radio_dis.append(r2)
        tab5.append(hbox_radio_dis)

        lbl_err = Gtk.Label(label="Entries con estado warning/error (mapeados a rojo/ámbar Everforest):")
        lbl_err.set_xalign(0.0)
        lbl_err.set_margin_top(10)
        tab5.append(lbl_err)

        entry_warn = Gtk.Entry()
        entry_warn.set_text("Entry en estado warning")
        entry_warn.add_css_class("warning")
        tab5.append(entry_warn)

        entry_err = Gtk.Entry()
        entry_err.set_text("Entry en estado error")
        entry_err.add_css_class("error")
        tab5.append(entry_err)

        lbl_lb = Gtk.Label(label="LevelBar lleno (mapeado a verde #A7C080) y al 45%:")
        lbl_lb.set_xalign(0.0)
        lbl_lb.set_margin_top(10)
        tab5.append(lbl_lb)

        lb1 = Gtk.LevelBar.new()
        lb1.set_min_value(0)
        lb1.set_max_value(100)
        lb1.add_offset_value("low", 25.0)
        lb1.add_offset_value("high", 75.0)
        lb1.add_offset_value("full", 90.0)
        lb1.set_value(100.0)
        tab5.append(lb1)

        lb2 = Gtk.LevelBar.new()
        lb2.set_min_value(0)
        lb2.set_max_value(100)
        lb2.add_offset_value("low", 25.0)
        lb2.add_offset_value("high", 75.0)
        lb2.add_offset_value("full", 90.0)
        lb2.set_value(45.0)
        tab5.append(lb2)

        lbl_pb = Gtk.Label(label="ProgressBar al 66%:")
        lbl_pb.set_xalign(0.0)
        tab5.append(lbl_pb)

        pb = Gtk.ProgressBar()
        pb.set_fraction(0.66)
        pb.set_text("66%")
        pb.set_show_text(True)
        tab5.append(pb)

        lbl_info = Gtk.Label(label="InfoBars (fondo #384B55 info / #45443C warning):")
        lbl_info.set_xalign(0.0)
        lbl_info.set_margin_top(10)
        tab5.append(lbl_info)

        for msg_type in (Gtk.MessageType.INFO, Gtk.MessageType.WARNING):
            ib = Gtk.InfoBar()
            ib.set_message_type(msg_type)
            ib.add_child(Gtk.Label(label=f"InfoBar {str(msg_type).split('.')[-1]} - fondos mapeados Everforest"))
            ib.set_revealed(True)
            tab5.append(ib)

        notebook.append_page(tab5, Gtk.Label(label="Links y Estados"))

        # --- PESTAÑA 6: Foco y Selección ---
        tab6 = new_tab()

        lbl_sel = Gtk.Label(label="Selección enfocada (selection:focus-within verde, texto #272E33,\nregla GTK4-only de overrides-gtk4.css):")
        lbl_sel.set_xalign(0.0)
        tab6.append(lbl_sel)

        entry_sel = Gtk.Entry()
        entry_sel.set_text("Texto seleccionado dentro de una Entry enfocada")
        entry_sel.connect("realize", lambda w: (w.select_region(0, -1), w.grab_focus()))
        tab6.append(entry_sel)

        lbl_tv = Gtk.Label(label="Selección en TextView:")
        lbl_tv.set_xalign(0.0)
        lbl_tv.set_margin_top(8)
        tab6.append(lbl_tv)

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
        tab6.append(scrolled_sel)

        lbl_spin = Gtk.Label(label="SpinButton enfocado:")
        lbl_spin.set_xalign(0.0)
        lbl_spin.set_margin_top(8)
        tab6.append(lbl_spin)

        spin = Gtk.SpinButton.new_with_range(0, 10, 1)
        spin.set_value(4)
        tab6.append(spin)

        lbl_focus = Gtk.Label(label="Pulsa Tab para ver el anillo de foco verde (focus-visible, overrides-gtk4.css):")
        lbl_focus.set_xalign(0.0)
        lbl_focus.set_margin_top(10)
        tab6.append(lbl_focus)

        btn_focus = Gtk.Button(label="Botón con anillo de foco verde (outline rgba(167,192,128,0.7))")
        tab6.append(btn_focus)

        dropdown = Gtk.DropDown.new_from_strings(["Opción de dropdown 1", "Opción de dropdown 2"])
        dropdown.set_selected(0)
        tab6.append(dropdown)

        notebook.append_page(tab6, Gtk.Label(label="Foco y Selección"))

        win.present()

    app = Gtk.Application(application_id="org.everforest.adwaita.visualtest")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])
