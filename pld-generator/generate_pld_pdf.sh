#!/bin/bash

# generate PLD's markdown
echo "Generating PLD in markdown..."
python3 main.py
# convert markdown to pdf
echo "Converting markdown to PDF..." 
gh-md-to-html pld.md -p pld.pdf -o OFFLINE
echo "Done"
