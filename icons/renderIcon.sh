#!/bin/sh

### Simple script to render a multi-resolution icon using 
### ImageMagick/convert

if [ -z $2 ]; then
    echo "Usage ${0} inputFile outputfile"
    exit
fi

echo "Converting $1"
convert $1  -bordercolor white -border 0 \
           \( -clone 0 -resize 64x64 \) \
           \( -clone 0 -resize 56x56 \) \
           \( -clone 0 -resize 48x48 \) \
           \( -clone 0 -resize 40x40 \) \
           \( -clone 0 -resize 32x32 \) \
           \( -clone 0 -resize 16x16 \) \
           -delete 0 -alpha off -colors 256 $2
