.PHONY: all compile clean test-gtk3 test-gtk4

all: compile

compile:
	python3 src/compile_theme.py

clean:
	rm -rf gtk-3.0/gtk.css gtk-3.0/gtk-dark.css gtk-3.0/assets gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gtk-4.0/assets

test-gtk3: compile
	chmod +x tests/test_switch.py
	python3 tests/test_switch.py --gtk3

test-gtk4: compile
	chmod +x tests/test_switch.py
	python3 tests/test_switch.py --gtk4
