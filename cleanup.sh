#!/bin/bash
cd /tmp/gifmovie
rm 00000m.png 00014m.png 00028m.png 00042m.png 00056m.png 00070m.png 00084m.png 00098m.png
convert 0*.png -gravity Center -crop 500x280+20-20\!  -delay 12 -loop 0 label.gif














