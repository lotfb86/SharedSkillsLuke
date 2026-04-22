#!/usr/bin/env bash
# build_outputs.sh — convert a dev-onboarding markdown doc to .docx and .pdf
#
# Usage: build_outputs.sh <input.md>
#
# Produces <input>.docx and <input>.pdf alongside the source markdown.
# Uses the Letter-sized reference docx in ../templates for tighter margins.
# Does NOT generate a pandoc TOC (field doesn't populate cleanly in LibreOffice PDF export).

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <input.md>" >&2
    exit 1
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: input file not found: $INPUT" >&2
    exit 1
fi

# Derive output paths from the input filename
BASENAME="${INPUT%.md}"
DOCX_OUT="${BASENAME}.docx"
PDF_OUT="${BASENAME}.pdf"

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REFERENCE_DOCX="${SCRIPT_DIR}/../templates/reference_letter.docx"

if [[ ! -f "$REFERENCE_DOCX" ]]; then
    echo "Error: reference docx not found at $REFERENCE_DOCX" >&2
    exit 1
fi

# Dependency checks
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc not installed. Run: brew install pandoc" >&2
    exit 1
fi

if ! command -v soffice &> /dev/null; then
    echo "Warning: soffice (LibreOffice) not found. Will skip PDF generation." >&2
    SKIP_PDF=1
else
    SKIP_PDF=0
fi

# --- Step 1: Markdown → DOCX ---
echo "→ Converting to .docx..."
pandoc "$INPUT" \
    -o "$DOCX_OUT" \
    --from gfm \
    --to docx \
    --reference-doc="$REFERENCE_DOCX" \
    --columns=120

echo "  Wrote $DOCX_OUT"

# --- Step 2: DOCX → PDF ---
if [[ $SKIP_PDF -eq 0 ]]; then
    echo "→ Converting to .pdf..."
    # soffice needs an output directory, not a file path
    OUT_DIR="$( dirname "$DOCX_OUT" )"
    soffice --headless --convert-to pdf --outdir "$OUT_DIR" "$DOCX_OUT" > /dev/null 2>&1
    echo "  Wrote $PDF_OUT"
fi

# --- Summary ---
echo ""
echo "Done. Files produced:"
echo "  markdown: $INPUT"
echo "  docx:     $DOCX_OUT"
if [[ $SKIP_PDF -eq 0 ]]; then
    echo "  pdf:      $PDF_OUT"
    # Report page count for quick sanity check
    if command -v pdfinfo &> /dev/null; then
        PAGES=$(pdfinfo "$PDF_OUT" | grep -E "^Pages:" | awk '{print $2}')
        echo "  (${PAGES} pages, US Letter)"
    fi
fi
