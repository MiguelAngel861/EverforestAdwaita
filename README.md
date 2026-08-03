# EverforestAdwaita

Un tema GTK programático basado en **Adwaita** con la paleta de colores **Everforest Dark Hard**, bordes rectos (esquinas de 90 grados) y mejoras de contraste para ventanas inactivas (*backdrop*). 

Este tema es compatible tanto con **GTK 3** como con **GTK 4**. Funciona interceptando los estilos CSS de Adwaita que vienen integrados en el sistema, reemplazando su paleta de colores por la de Everforest mediante un script en Python y aplicando una hoja de estilos de personalización extra.

---

## Características principales

- **Compatibilidad Dual:** Genera directorios de estilo independientes y válidos para GTK 3 y GTK 4.
- **Esquinas Cuadradas:** Eliminación completa de bordes redondeados en ventanas, botones, menús, campos de texto y decoraciones del cliente (CSD).
- **Alto Contraste en Selección:** Estilo exhaustivo para elementos seleccionados con colores bien definidos para estados activo, inactivo (backdrop) y enfocado.
- **Soporte para Ventanas Inactivas (Backdrop):** Reglas específicas para reducir el contraste y cambiar el tono de las ventanas desenfocadas, facilitando la concentración y mejorando la usabilidad en entornos multimonitor.
- **Scrollbars Minimalistas:** Barras de desplazamiento delgadas y discretas que reaccionan sutilmente al pasar el cursor o hacer clic.
- **Botones de Acción Semánticos:** Estilo personalizado para botones de acción sugerida (`suggested-action`, verde) y destructiva (`destructive-action`, rojo) alineados con la estética Everforest.

---

## Estructura del proyecto

```text
EverforestAdwaita/
├─ src/
│  ├─ colors.json        # Mapeo de colores hexadecimales (Adwaita -> Everforest)
│  ├─ overrides.css      # Reglas personalizadas (esquinas, scrollbars, contrastes, backdrop)
│  └─ compile_theme.py   # Script compilador en Python
├─ Makefile              # Automatización para compilar y limpiar
├─ index.theme           # Metadatos del tema para el entorno de escritorio
└─ README.md             # Este archivo
```

---

## Requisitos del sistema

Para poder compilar el tema, necesitas tener instalado Python 3 junto con los bindings de GObject (`PyGObject` / `gi`) y las librerías de GTK del sistema:

### En Arch Linux
```bash
sudo pacman -S python-gobject gtk3 gtk4
```

### En Debian / Ubuntu
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtk-4.0
```

---

## Instalación para desarrollo local (Recomendado)

Para poder desarrollar y ver tus cambios al instante, se recomienda enlazar simbólicamente este repositorio de desarrollo a tu directorio de temas de usuario (`~/.local/share/themes/`):

1. **Clona el repositorio** en tu carpeta de proyectos preferida.
2. **Crea el enlace simbólico** (reemplaza la ruta si es necesario):
   ```bash
   ln -s "$PWD" "$HOME/.local/share/themes/EverforestAdwaita"
   ```
3. **Compila el tema** por primera vez:
   ```bash
   make compile
   ```

Esto generará las carpetas `gtk-3.0/` y `gtk-4.0/` directamente dentro de tu espacio de trabajo, haciéndolas accesibles al sistema de inmediato.

---

## Aplicar y probar el tema

### 1. Aplicación global / de usuario
Puedes utilizar herramientas gráficas como **`nwg-look`** (en Wayland / wlroots) o **GNOME Tweaks** para seleccionar el tema `EverforestAdwaita`.

También puedes aplicarlo directamente desde la terminal mediante `gsettings`:
```bash
gsettings set org.gnome.desktop.interface gtk-theme "EverforestAdwaita"
```

### 2. Forzar recarga rápida tras compilar
Si realizas un cambio en `src/overrides.css` o `src/colors.json`, ejecutas `make compile` y quieres que las aplicaciones abiertas actualicen sus estilos sin tener que reiniciarlas, puedes forzar una recarga rápida alternando el tema:

```bash
gsettings set org.gnome.desktop.interface gtk-theme "Adwaita" && gsettings set org.gnome.desktop.interface gtk-theme "EverforestAdwaita"
```

### 3. Probar aplicaciones individuales
Si quieres testear el tema en una aplicación concreta sin cambiar la configuración global del sistema:

- **Para GTK 3 (ej. gedit):**
  ```bash
  GTK_THEME=EverforestAdwaita gedit
  ```
- **Para GTK 4 (ej. gnome-calculator):**
  ```bash
  GTK_THEME=EverforestAdwaita gnome-calculator
  ```

---

## Flujo de trabajo de desarrollo

1. Realiza cambios en los archivos de configuración:
   - Modifica [overrides.css](file:///home/damian/Projects/EverforestAdwaita/src/overrides.css) para ajustar márgenes, bordes, sombras o estados.
   - Modifica [colors.json](file:///home/damian/Projects/EverforestAdwaita/src/colors.json) si deseas alterar el mapeo de colores base de Adwaita.
2. Ejecuta `make compile` para regenerar los archivos `gtk.css`.
3. Refresca tu entorno o aplicaciones para verificar el resultado.