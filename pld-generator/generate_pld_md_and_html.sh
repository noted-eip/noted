#!/bin/bash

# generate PLD's markdown
echo "Generating PLD in markdown..."
python3 main.py
# convert markdown to pdf
echo "Converting markdown to HTML..." 
gh-md-to-html -o OFFLINE pld.md
echo "Converting markdown to HTML..." 
sed -i "s/\\/images/.\\/images/g" pld.html
sed -i "s/\\/github-markdown-css/.\\/github-markdown-css/g" pld.html
echo "Done"
