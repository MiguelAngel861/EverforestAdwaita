# Python con PyGObject (gi) para compilar y testear: el python del sistema
PYTHON := python3

# Python con watchdog para el watcher: .venv (pip user-local para evitar externally-managed)
WATCH_PYTHON := .venv/bin/python

.PHONY: all compile clean validate baseline-update \
        test-gtk3 test-gtk4 \
        test-switch-gtk3 test-switch-gtk4 \
        test-components-gtk3 test-components-gtk4 \
        test-changes-gtk3 test-changes-gtk4 \
        test-disabled-gtk3 test-disabled-gtk4 \
        watch

all: compile

compile:
	$(PYTHON) src/compile_theme.py

validate: compile
	$(PYTHON) tests/test_validate.py

baseline-update:
	sha256sum gtk-3.0/gtk.css gtk-4.0/gtk.css > docs/baseline.sha256

clean:
	rm -rf gtk-3.0/gtk.css gtk-3.0/gtk-dark.css gtk-3.0/assets gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gtk-4.0/assets

# Atajos al tester de switch (históricos)
test-gtk3: test-switch-gtk3
test-gtk4: test-switch-gtk4

# Testers visuales explícitos (reglas literales: el completado de make no debe ver plantillas)
test-switch-gtk3: compile
	chmod +x tests/test_switch.py
	$(PYTHON) tests/test_switch.py --gtk3

test-switch-gtk4: compile
	chmod +x tests/test_switch.py
	$(PYTHON) tests/test_switch.py --gtk4

test-components-gtk3: compile
	chmod +x tests/test_components.py
	$(PYTHON) tests/test_components.py --gtk3

test-components-gtk4: compile
	chmod +x tests/test_components.py
	$(PYTHON) tests/test_components.py --gtk4

test-changes-gtk3: compile
	chmod +x tests/test_changes.py
	$(PYTHON) tests/test_changes.py --gtk3

test-changes-gtk4: compile
	chmod +x tests/test_changes.py
	$(PYTHON) tests/test_changes.py --gtk4

test-disabled-gtk3: compile
	chmod +x tests/test_disabled.py
	$(PYTHON) tests/test_disabled.py --gtk3

test-disabled-gtk4: compile
	chmod +x tests/test_disabled.py
	$(PYTHON) tests/test_disabled.py --gtk4

watch:
	$(WATCH_PYTHON) scripts/watcher.py
