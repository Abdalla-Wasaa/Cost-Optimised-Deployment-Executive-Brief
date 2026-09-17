# Executive brief export
The authoritative source is executive_brief.md. The adjacent HTML is a printable
one-page layout, with no external fonts or scripts. Open executive_brief.html in
Chrome/Edge → Print → Save as PDF → A4 portrait, scale 100%, headers/footers off.
Inspect the preview and choose one page before saving executive_brief.pdf.

Optional installed Chromium CLI, run from Capstone_week7:

```bash
chromium --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/exec/executive_brief.pdf" \
  "file://$PWD/exec/executive_brief.html"
```

Do not label an export as reviewed until text, page count and figures are inspected.

## Reproduce the supplied PDF and HTML from the Markdown source

```bash
python -m pip install -r exec/requirements-export.txt
python -m scripts.render_brief
```

The supplied PDF was generated with ReportLab, confirmed to contain one page and
visually inspected. ReportLab is an optional export dependency, not a service or
CI dependency. Export regenerates both HTML and PDF from the same Markdown.
