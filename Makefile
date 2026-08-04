# Python del entorno uv (Python 3.13 + PyGObject en .venv): compilar y testear
PYTHON := .venv/bin/python
WATCH_PYTHON := .venv/bin/python

.PHONY: all setup compile clean validate baseline-update test-gtk3 test-gtk4 watch

all: compile

setup:
	uv sync

compile:
	$(PYTHON) src/compile_theme.py

validate: compile
	$(PYTHON) tests/test_validate.py

baseline-update:
	sha256sum gtk-3.0/gtk.css gtk-4.0/gtk.css > docs/baseline.sha256

clean:
	rm -rf gtk-3.0/gtk.css gtk-3.0/gtk-dark.css gtk-3.0/assets gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gtk-4.0/assets

# Tester visual unificado (6 pestañas): switch, checkbox, botones, popovers,
# diálogos, vistas, tooltips/menús, deshabilitados, links, barras, foco y selección
test-gtk3: compile
	chmod +x tests/test_visual.py
	$(PYTHON) tests/test_visual.py --gtk3

test-gtk4: compile
	chmod +x tests/test_visual.py
	$(PYTHON) tests/test_visual.py --gtk4

watch:
	$(WATCH_PYTHON) scripts/watcher.py
