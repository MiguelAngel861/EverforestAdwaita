#!/usr/bin/env python3
"""Validación no-visual del tema compilado.

Comprueba:
1. Parseo estricto de gtk-3.0/gtk.css y gtk-4.0/gtk.css con Gtk.CssProvider
   (detecta "Junk at end of value" y propiedades no válidas).
2. Paridad de hashes contra docs/baseline.sha256 (aviso si cambió sin actualizar baseline).
3. Hexes del CSS base de Adwaita sin mapear en colors.json (aviso informativo).

Requiere display gráfico para el parseo (Gtk.init), igual que los testers visuales.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
BASELINE_FILE = os.path.join(DOCS_DIR, "baseline.sha256")

# Añadir el compilador al path para reutilizar la auditoría de hexes
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
from compiler.adwaita import extract_css_base  # noqa: E402
from compiler.palette import audit_unmapped_hexes  # noqa: E402


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_css(gtk_version):
    """Parsea gtk.css con Gtk.CssProvider en un subprocess aislado.

    Devuelve (ok, errores) donde errores son las líneas problemáticas de stderr.
    """
    gi_version = "3.0" if gtk_version == "3" else "4.0"
    css_path = os.path.join(REPO_ROOT, f"gtk-{gtk_version}.0", "gtk.css")
    if not os.path.exists(css_path):
        return False, [f"No se encontró {css_path}; ejecuta 'make compile' primero"]

    py_code = f"""
import gi, sys
gi.require_version('Gtk', '{gi_version}')
from gi.repository import Gtk
Gtk.init({'[]' if gtk_version == '3' else ''})
try:
    provider = Gtk.CssProvider()
    provider.load_from_path('{css_path}')
    print("PARSE_OK")
except Exception as e:
    print(f"PARSE_FAIL: {{e}}")
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", py_code], capture_output=True, text=True, check=False)
    stderr_lines = [ln for ln in result.stderr.splitlines() if ln.strip()]
    if "PARSE_OK" in result.stdout:
        return True, stderr_lines
    return False, stderr_lines + result.stdout.splitlines()


def load_baseline():
    """Lee docs/baseline.sha256 como dict path -> hash."""
    baseline = {}
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    baseline[parts[1]] = parts[0]
    return baseline


def check_baseline():
    """Compara los CSS actuales contra el baseline. Devuelve lista de avisos."""
    baseline = load_baseline()
    warnings = []
    for subdir, rel in (("gtk-3.0", "gtk-3.0/gtk.css"), ("gtk-4.0", "gtk-4.0/gtk.css")):
        path = os.path.join(REPO_ROOT, subdir, "gtk.css")
        if not os.path.exists(path):
            warnings.append(f"No existe {rel}; ejecuta 'make compile' primero")
            continue
        current = sha256_file(path)
        expected = baseline.get(rel)
        if expected is None:
            warnings.append(f"{rel}: sin entrada en baseline (ejecuta 'make baseline-update')")
        elif current != expected:
            warnings.append(
                f"{rel}: el hash cambió ({current[:12]} != {expected[:12]}). "
                "Si el cambio es intencional, actualiza el baseline con 'make baseline-update'"
            )
    return warnings


def check_unmapped_hexes():
    """Extrae el base de Adwaita y reporta hexes sin mapear. Devuelve lista de avisos."""
    warnings = []
    try:
        from compiler.theme import load_theme
        from pathlib import Path

        theme = load_theme(Path(REPO_ROOT) / "src" / "themes" / "everforest-adwaita")
        for gtk in ("3", "4"):
            base = extract_css_base(gtk)
            unmapped = audit_unmapped_hexes(base.css_content, theme.colors_map)
            suspicious = {h for h in unmapped if h not in ("#ffffff", "#000000", "#fff", "#000")}
            if suspicious:
                warnings.append(
                    f"GTK {gtk}: hexes de Adwaita sin mapear en colors.json: {sorted(suspicious)}"
                )
    except Exception as e:
        warnings.append(f"No se pudo auditar hexes: {e}")
    return warnings


def main():
    failed = False
    all_warnings = []

    print("=== Validación de parseo estricto (GTK 3 y GTK 4) ===")
    for gtk in ("3", "4"):
        ok, errors = parse_css(gtk)
        if ok:
            print(f"  GTK {gtk}: CSS parsea correctamente"
                  + (f" ({len(errors)} warnings tolerados)" if errors else ""))
            for err in errors:
                print(f"    warning: {err[:120]}")
        else:
            print(f"  GTK {gtk}: ERROR al parsear CSS")
            for err in errors:
                print(f"    {err[:120]}")
            failed = True

    print("=== Paridad con baseline ===")
    baseline_warnings = check_baseline()
    if baseline_warnings:
        for w in baseline_warnings:
            print(f"  AVISO: {w}")
            all_warnings.append(w)
    else:
        print("  OK: hashes idénticos al baseline")

    print("=== Auditoría de hexes sin mapear ===")
    hex_warnings = check_unmapped_hexes()
    if hex_warnings:
        for w in hex_warnings:
            print(f"  AVISO: {w}")
            all_warnings.append(w)
    else:
        print("  OK: todos los hexes del base de Adwaita están mapeados")

    if failed:
        print("\nRESULTADO: FAIL (errores de parseo)")
        sys.exit(1)
    if all_warnings:
        print(f"\nRESULTADO: OK con {len(all_warnings)} avisos (no bloqueantes)")
        sys.exit(0)
    print("\nRESULTADO: OK sin avisos")
    sys.exit(0)


if __name__ == "__main__":
    main()