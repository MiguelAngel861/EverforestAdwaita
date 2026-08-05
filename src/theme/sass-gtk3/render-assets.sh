#!/bin/bash

INKSCAPE="inkscape"

SRC_FILE="assets.svg"
ASSETS_DIR="assets"
INDEX="assets.txt"

optimize_png() {
    if command -v optipng >/dev/null 2>&1; then
        optipng -o7 --quiet "$1"
    fi
}

for i in `cat $INDEX`
do 
if [ -f $ASSETS_DIR/$i.png ]; then
    echo $ASSETS_DIR/$i.png exists.
else
    echo
    echo Rendering $ASSETS_DIR/$i.png
    $INKSCAPE --export-id=$i \
              --export-id-only \
              --export-type="png" \
              --export-filename=$ASSETS_DIR/$i.png $SRC_FILE >/dev/null
    optimize_png $ASSETS_DIR/$i.png
fi
if [ -f $ASSETS_DIR/$i@2.png ]; then
    echo $ASSETS_DIR/$i@2.png exists.
else
    echo
    echo Rendering $ASSETS_DIR/$i@2.png
    $INKSCAPE --export-id=$i \
              --export-dpi=180 \
              --export-id-only \
              --export-type="png" \
              --export-filename=$ASSETS_DIR/$i@2.png $SRC_FILE >/dev/null
    optimize_png $ASSETS_DIR/$i@2.png
fi
done
exit 0

