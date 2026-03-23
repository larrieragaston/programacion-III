#!/usr/bin/env bash
# Starts the index server and all Slidev presentations automatically.
# Each presentation gets a sequential port starting from 3031.
# The index page runs on port 3030.

set -e

INDEX_PORT=3030
SLIDE_PORT=3031
COMMANDS=()
NAMES=()

NAMES+=("index")
COMMANDS+=("npx serve . -l $INDEX_PORT --cors --no-clipboard")

for dir in */; do
  if [ -f "${dir}package.json" ] && grep -q "slidev" "${dir}package.json"; then
    name="${dir%/}"
    NAMES+=("$name")
    COMMANDS+=("cd $dir && npx slidev --port $SLIDE_PORT")
    SLIDE_PORT=$((SLIDE_PORT + 1))
  fi
done

echo ""
echo "  Starting development servers..."
echo "  Index:  http://localhost:$INDEX_PORT"
echo ""

npx concurrently --names "$(IFS=,; echo "${NAMES[*]}")" --prefix-colors "blue,green,yellow,cyan,magenta" --kill-others "${COMMANDS[@]}"
