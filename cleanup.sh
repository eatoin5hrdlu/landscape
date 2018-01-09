#!/bin/bash
cd /tmp/gifmovie
rm 00000m.png 00014m.png 00028m.png 00042m.png 00056m.png 00070m.png 00084m.png 00097m.png 00111m.png 00125m.png 00139m.png 00153m.png
convert 0*.png -gravity Center -crop 500x280+20-20\!  -delay 12 -loop 0 blabel.gif














