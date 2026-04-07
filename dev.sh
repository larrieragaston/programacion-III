#!/usr/bin/env bash
# Starts the index server and all Slidev presentations with fixed ports.
# Also refreshes exported PDFs before startup unless DISABLE_EXPORTS_ON_DEV=1.

set -euo pipefail

INDEX_PORT=3030
EXPORT_ON_DEV="${DISABLE_EXPORTS_ON_DEV:-0}"

MODULES=("introduction" "lambda-calculus" "fp-backus" "clojure")
PORTS=("3031" "3032" "3033" "3034")

function export_module_pdf() {
  local module="$1"

  if [ ! -d "$module" ] || [ ! -f "$module/package.json" ]; then
    return 0
  fi

  echo "  Exporting ${module}..."
  if (
    cd "$module"
    npm run export
  ); then
    return 0
  fi

  echo "  Playwright missing for ${module}. Installing browser exporter dependencies..."
  (
    cd "$module"
    npm i -D playwright-chromium
    npx playwright install chromium
    npm run export
  )
}

if [ "$EXPORT_ON_DEV" = "0" ]; then
  echo ""
  echo "  Regenerating module exports..."
  for module in "${MODULES[@]}"; do
    export_module_pdf "$module"
  done
fi

COMMANDS=()
NAMES=()

NAMES+=("index")
COMMANDS+=("npx serve . -l $INDEX_PORT --cors --no-clipboard")

for i in "${!MODULES[@]}"; do
  module="${MODULES[$i]}"
  port="${PORTS[$i]}"

  if [ -f "${module}/package.json" ]; then
    NAMES+=("$module")
    COMMANDS+=("cd \"$module\" && npx slidev --port $port")
  fi
done

echo ""
echo "  Starting development servers..."
echo "  Index: http://localhost:$INDEX_PORT"
for i in "${!MODULES[@]}"; do
  module="${MODULES[$i]}"
  port="${PORTS[$i]}"
  if [ -f "${module}/package.json" ]; then
    echo "  ${module}: http://localhost:${port}"
  fi
done
echo ""

npx concurrently --names "$(IFS=,; echo "${NAMES[*]}")" --prefix-colors "blue,green,yellow,cyan,magenta" --kill-others "${COMMANDS[@]}"
