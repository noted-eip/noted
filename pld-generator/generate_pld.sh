#!/bin/bash

if [[ $# != "2" ]]
then
    echo "./generate_pld.sh [height_of_the_pdf] [pdf output]"
    exit 1
fi

# generate PLD's markdown
echo "Generating PLD in markdown..."
python3 main.py
# convert markdown to pdf
echo "Converting markdown to HTML..." 
gh-md-to-html -o OFFLINE pld.md
echo "Fixing relative paths..." 
sed -i "s/\\/images/.\\/images/g" pld.html
sed -i "s/\\/github-markdown-css/.\\/github-markdown-css/g" pld.html
wkhtmltopdf --enable-local-file-access --page-width 210mm --page-height "$1"mm --outline-depth 1 pld.html "$2"
echo "Done"
