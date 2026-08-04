#!/usr/bin/env python3
import sys
import os
import gi

sys.path.insert(0, os.path.dirname(__file__))
import common

use_gtk3 = common.parse_gtk_args()
common.load_css(use_gtk3)

if use_gtk3:
    print("Iniciando visualizador de componentes con GTK 3...")
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    
    Gtk.init([])
    
    # Crear Ventana Principal (Sombra Nivel 4)
    win = Gtk.Window(title="EverforestAdwaita - Visualizador GTK 3")
    win.set_default_size(500, 600)
    win.connect("destroy", Gtk.main_quit)
    
    # HeaderBar
    hb = Gtk.HeaderBar()
    hb.set_show_close_button(True)
    hb.set_title("Componentes Everforest")
    hb.set_subtitle("GTK 3 Shadow Testing")
    win.set_titlebar(hb)
    
    # Contenedor Principal
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    main_box.set_margin_top(15)
    main_box.set_margin_bottom(15)
    main_box.set_margin_start(15)
    main_box.set_margin_end(15)
    win.add(main_box)
    
    # Notebook para pestañas
    notebook = Gtk.Notebook()
    main_box.pack_start(notebook, True, True, 0)
    
    # --- PESTAÑA 1: Flotantes y Sombras ---
    tab1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    tab1_box.set_border_width(10)
    
    # Nivel 1: Tooltip
    btn_tooltip = Gtk.Button(label="Pasa el cursor aquí (Tooltip - Nivel 1)")
    btn_tooltip.set_tooltip_text("Este tooltip de información usa una sombra discreta de Nivel 1.")
    tab1_box.pack_start(btn_tooltip, False, False, 0)
    
    # Nivel 2: Popover
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
    tab1_box.pack_start(btn_popover, False, False, 0)
    
    # Nivel 2: ComboBox / Dropdown
    combo_box = Gtk.ComboBoxText()
    combo_box.append_text("Opción de Dropdown 1 (Nivel 2)")
    combo_box.append_text("Opción de Dropdown 2 (Nivel 2)")
    combo_box.append_text("Opción de Dropdown 3 (Nivel 2)")
    combo_box.set_active(0)
    tab1_box.pack_start(combo_box, False, False, 0)
    
    # Radio Buttons
    hbox_radio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
    lbl_radio = Gtk.Label(label="Selección Única (Radios Cuadrados):")
    lbl_radio.set_xalign(0.0)
    radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Opción A")
    radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Opción B")
    hbox_radio.pack_start(lbl_radio, True, True, 0)
    hbox_radio.pack_end(radio1, False, False, 0)
    hbox_radio.pack_end(radio2, False, False, 0)
    tab1_box.pack_start(hbox_radio, False, False, 0)
    
    # Nivel 3: Diálogo Modal
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
    tab1_box.pack_start(btn_dialog, False, False, 0)
    
    notebook.append_page(tab1_box, Gtk.Label(label="Flotantes y Sombras"))
    
    # --- PESTAÑA 2: Controles y Scrollbars ---
    tab2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    tab2_box.set_border_width(10)
    
    # Botones
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
    tab2_box.pack_start(btn_box, False, False, 0)
    
    # Inputs
    entry = Gtk.Entry()
    entry.set_placeholder_text("Escribe aquí... (Input en Foco)")
    tab2_box.pack_start(entry, False, False, 0)
    
    # Switch
    hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sw = Gtk.Label(label="Interruptor Everforest:")
    lbl_sw.set_xalign(0.0)
    sw = Gtk.Switch()
    hbox_sw.pack_start(lbl_sw, True, True, 0)
    hbox_sw.pack_end(sw, False, False, 0)
    tab2_box.pack_start(hbox_sw, False, False, 0)
    
    # Scrolled Window con ListBox (Prueba de Scrollbars y Selección)
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
    tab2_box.pack_start(scrolled, True, True, 0)
    
    notebook.append_page(tab2_box, Gtk.Label(label="Controles y Listas"))
    
    win.show_all()
    Gtk.main()

else:
    print("Iniciando visualizador de componentes con GTK 4...")
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk
    
    def on_activate(app):
        # Crear Ventana Principal (Sombra Nivel 4)
        win = Gtk.ApplicationWindow(application=app, title="EverforestAdwaita - Visualizador GTK 4")
        win.set_default_size(500, 600)
        
        # HeaderBar
        hb = Gtk.HeaderBar()
        hb.set_show_title_buttons(True)
        win.set_titlebar(hb)
        
        # Contenedor Principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        win.set_child(main_box)
        
        # Notebook para pestañas
        notebook = Gtk.Notebook()
        main_box.append(notebook)
        
        # --- PESTAÑA 1: Flotantes y Sombras ---
        tab1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        tab1_box.set_margin_top(10)
        tab1_box.set_margin_bottom(10)
        tab1_box.set_margin_start(10)
        tab1_box.set_margin_end(10)
        
        # Nivel 1: Tooltip
        btn_tooltip = Gtk.Button(label="Pasa el cursor aquí (Tooltip - Nivel 1)")
        btn_tooltip.set_tooltip_text("Este tooltip de información usa una sombra discreta de Nivel 1.")
        tab1_box.append(btn_tooltip)
        
        # Nivel 2: Popover
        btn_popover = Gtk.Button(label="Mostrar Popover (Nivel 2)")
        popover = Gtk.Popover()
        popover.set_parent(btn_popover)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        popover_content.set_margin_top(10)
        popover_content.set_margin_bottom(10)
        popover_content.set_margin_start(10)
        popover_content.set_margin_end(10)
        
        lbl_pop = Gtk.Label(label="Menú / Popover Flotante")
        popover_content.append(lbl_pop)
        
        pop_btn1 = Gtk.Button(label="Opción 1")
        pop_btn1.add_css_class("flat")
        pop_btn2 = Gtk.Button(label="Opción 2")
        pop_btn2.add_css_class("flat")
        popover_content.append(pop_btn1)
        popover_content.append(pop_btn2)
        popover.set_child(popover_content)
        
        btn_popover.connect("clicked", lambda w: popover.popup() if not popover.get_visible() else popover.popdown())
        tab1_box.append(btn_popover)
        
        # Nivel 2: ComboBox / Dropdown
        combo_box = Gtk.ComboBoxText()
        combo_box.append_text("Opción de Dropdown 1 (Nivel 2)")
        combo_box.append_text("Opción de Dropdown 2 (Nivel 2)")
        combo_box.append_text("Opción de Dropdown 3 (Nivel 2)")
        combo_box.set_active(0)
        tab1_box.append(combo_box)
        
        # Radio Buttons
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
        tab1_box.append(hbox_radio)
        
        # Nivel 3: Diálogo Modal
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
        tab1_box.append(btn_dialog)
        
        notebook.append_page(tab1_box, Gtk.Label(label="Flotantes y Sombras"))
        
        # --- PESTAÑA 2: Controles y Scrollbars ---
        tab2_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        tab2_box.set_margin_top(10)
        tab2_box.set_margin_bottom(10)
        tab2_box.set_margin_start(10)
        tab2_box.set_margin_end(10)
        
        # Botones
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
        tab2_box.append(btn_box)
        
        # Inputs
        entry = Gtk.Entry()
        entry.set_placeholder_text("Escribe aquí... (Input en Foco)")
        tab2_box.append(entry)
        
        # Switch
        hbox_sw = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_sw = Gtk.Label(label="Interruptor Everforest:")
        lbl_sw.set_xalign(0.0)
        sw = Gtk.Switch()
        sw.set_halign(Gtk.Align.END)
        hbox_sw.append(lbl_sw)
        lbl_sw.set_hexpand(True)
        hbox_sw.append(sw)
        tab2_box.append(hbox_sw)
        
        # Scrolled Window con ListBox (Prueba de Scrollbars y Selección)
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
            lbl_row = Gtk.Label(label=f"Fila {i} - Elemento de Lista Seleccionable")
            row_box.append(lbl_row)
            row.set_child(row_box)
            listbox.append(row)
            
        scrolled.set_child(listbox)
        tab2_box.append(scrolled)
        
        notebook.append_page(tab2_box, Gtk.Label(label="Controles y Listas"))
        
        win.present()
        
    app = Gtk.Application(application_id="org.everforest.adwaita.componenttest")
    app.connect("activate", on_activate)
    app.run([sys.argv[0]])
