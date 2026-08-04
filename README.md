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
│  ├─ compiler/                # Compilador modular
│  │  ├─ theme.py              # Carga y validación de theme.json + colors.json
│  │  ├─ adwaita.py            # Extracción CSS base + assets (GResources), cache y detección de cambios
│  │  ├─ palette.py            # Aplicación del mapa de colores + auditoría de hexes sin mapear
│  │  └─ build.py              # Ensamblaje final (base mapeado + overrides) y CLI
│  ├─ themes/
│  │  └─ everforest-adwaita/   # Tema (estructura lista para temas hermanos)
│  │     ├─ theme.json         # Metadatos del tema (versiones GTK, archivos, requisitos)
│  │     ├─ colors.json        # Mapeo de colores hexadecimales (Adwaita -> Everforest)
│  │     ├─ overrides.css      # Reglas personalizadas (esquinas, scrollbars, contrastes, backdrop)
│  │     ├─ overrides-gtk3.css # Reglas solo-GTK 3 (ej. -gtk-outline-radius)
│  │     └─ overrides-gtk4.css # Reglas solo-GTK 4 (anillos de foco, selección enfocada)
│  └─ compile_theme.py         # CLI: python3 src/compile_theme.py [--theme X] [--gtk3|--gtk4]
├─ gtk-3.0/                    # CSS y assets compilados (GTK 3)
├─ gtk-4.0/                    # CSS y assets compilados (GTK 4)
├─ build/cache/                # Cache del CSS base de Adwaita + diffs (generado, gitignored)
├─ tests/
│  ├─ common.py                # Infraestructura compartida (--gtk3/--gtk4, carga CSS)
│  ├─ test_validate.py         # Validación no-visual (parseo estricto, baseline, auditoría)
│  ├─ test_switch.py           # Testers visuales (adelgazados, usan common.py)
│  ├─ test_components.py
│  ├─ test_changes.py
│  └─ test_disabled.py
├─ scripts/watcher.py          # Auto-compila al guardar cambios en src/themes/ y src/compiler/
├─ docs/
│  ├─ baseline.sha256          # Hashes de referencia del CSS compilado
│  └─ adwaita-version.txt      # Versiones GTK usadas para el baseline
├─ Makefile                    # compile, validate, test-*, watch
├─ index.theme                 # Metadatos del tema para el entorno de escritorio
└─ README.md                   # Este archivo
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
Si realizas un cambio en los archivos de `src/themes/everforest-adwaita/`, ejecutas `make compile` y quieres que las aplicaciones abiertas actualicen sus estilos sin tener que reiniciarlas, puedes forzar una recarga rápida alternando el tema:

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

1. Realiza cambios en los archivos de configuración del tema (en `src/themes/everforest-adwaita/`):
   - Modifica [overrides.css](file:///home/damian/Projects/EverforestAdwaita/src/themes/everforest-adwaita/overrides.css) para ajustar márgenes, bordes, sombras o estados.
   - Modifica [colors.json](file:///home/damian/Projects/EverforestAdwaita/src/themes/everforest-adwaita/colors.json) si deseas alterar el mapeo de colores base de Adwaita.
   - Usa `overrides-gtk3.css` / `overrides-gtk4.css` para reglas válidas solo en una versión.
2. Ejecuta `make compile` para regenerar los archivos `gtk.css`.
3. Ejecuta `make validate` para comprobar que el CSS parsea correctamente en GTK 3 y GTK 4,
   que los hashes coinciden con el baseline y ver la auditoría de hexes sin mapear.
4. Refresca tu entorno o aplicaciones para verificar el resultado.

### Baseline y paridad

- `docs/baseline.sha256` guarda los hashes de `gtk-3.0/gtk.css` y `gtk-4.0/gtk.css`
  compilados como referencia.
- `make validate` avisa si el CSS compilado cambia sin actualizar el baseline
  (señal de cambio no intencional).
- Si el cambio es intencional (ej. un override nuevo), actualiza el baseline con
  `make baseline-update`.

### Crear un tema hermano

La estructura soporta múltiples temas en `src/themes/<nombre>/`. Para crear uno nuevo:

1. Copia `src/themes/everforest-adwaita/` a `src/themes/<nombre>/`.
2. Adapta `colors.json` (paleta y mapa), los `overrides*.css` y `theme.json`.
3. Compila con `python3 src/compile_theme.py --theme <nombre>`.

### Watch automático

Ejecuta `make watch` (requiere `pip install watchdog` en `.venv/`) para que el tema
se recompile automáticamente al guardar cambios en `src/themes/` o `src/compiler/`.