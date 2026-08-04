.PHONY: all compile clean validate baseline-update test-gtk3 test-gtk4 test-components-gtk3 test-components-gtk4 test-changes-gtk3 test-changes-gtk4 test-disabled-gtk3 test-disabled-gtk4 watch

all: compile

compile:
	python3 src/compile_theme.py

validate: compile
	python3 tests/test_validate.py

baseline-update:
	sha256sum gtk-3.0/gtk.css gtk-4.0/gtk.css > docs/baseline.sha256

clean:
	rm -rf gtk-3.0/gtk.css gtk-3.0/gtk-dark.css gtk-3.0/assets gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gtk-4.0/assets

test-gtk3: compile
	chmod +x tests/test_switch.py
	python3 tests/test_switch.py --gtk3

test-gtk4: compile
	chmod +x tests/test_switch.py
	python3 tests/test_switch.py --gtk4

test-components-gtk3: compile
	chmod +x tests/test_components.py
	python3 tests/test_components.py --gtk3

test-components-gtk4: compile
	chmod +x tests/test_components.py
	python3 tests/test_components.py --gtk4

test-changes-gtk3: compile
	chmod +x tests/test_changes.py
	python3 tests/test_changes.py --gtk3

test-changes-gtk4: compile
	chmod +x tests/test_changes.py
	python3 tests/test_changes.py --gtk4

test-disabled-gtk3: compile
	chmod +x tests/test_disabled.py
	python3 tests/test_disabled.py --gtk3

test-disabled-gtk4: compile
	chmod +x tests/test_disabled.py
	python3 tests/test_disabled.py --gtk4

watch:
	.venv/bin/python scripts/watcher.py
