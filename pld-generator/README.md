# PLD Generator

## PDF generation

You will need [`gh-md-to-html`](https://github.com/phseiff/github-flavored-markdown-to-html) with it's pdf export module and offline conversion (for convenience purposes).

## GITHUB_OAUTH_TOKEN

You need to set a `GITHUB_OAUTH_TOKEN` env variable which has the permission to read the organizations and issues from this organization.

## Formatter

We're using `black`-style and it's binary to format the source code. We just deactivate it for graphql multi-line string requests, that's why you will see `#fmt: off` ans `#fmt: on` in `src/github.py`. 

