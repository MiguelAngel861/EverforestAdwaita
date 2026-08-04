# Python con PyGObject (gi) para compilar y testear: el python del sistema
PYTHON := python3

# Python con watchdog para el watcher: .venv (pip user-local para evitar externally-managed)
WATCH_PYTHON := .venv/bin/python

# Scripts de test (sin extensión .py)
TESTS := switch components changes disabled
TEST_TARGETS := $(foreach t,$(TESTS),test-$(t)-gtk3 test-$(t)-gtk4)

.PHONY: all compile clean validate baseline-update $(TEST_TARGETS) watch

all: compile

compile:
	$(PYTHON) src/compile_theme.py

validate: compile
	$(PYTHON) tests/test_validate.py

baseline-update:
	sha256sum gtk-3.0/gtk.css gtk-4.0/gtk.css > docs/baseline.sha256

clean:
	rm -rf gtk-3.0/gtk.css gtk-3.0/gtk-dark.css gtk-3.0/assets gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gtk-4.0/assets

# Targets genéricos: test-<nombre>-gtk3 / test-<nombre>-gtk4
define test_template
test-$(1)-gtk3: compile
	chmod +x tests/test_$(1).py
	$(PYTHON) tests/test_$(1).py --gtk3

test-$(1)-gtk4: compile
	chmod +x tests/test_$(1).py
	$(PYTHON) tests/test_$(1).py --gtk4
endef
$(foreach t,$(TESTS),$(eval $(call test_template,$(t))))

watch:
	$(WATCH_PYTHON) scripts/watcher.py
