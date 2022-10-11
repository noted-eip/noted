#!/bin/bash

# generate PLD's markdown
python3 main.py
# convert markdown to pdf
gh-md-to-html pld.md -p pld.pdf -o OFFLINE
