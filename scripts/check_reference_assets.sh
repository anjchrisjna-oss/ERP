#!/usr/bin/env bash
set -euo pipefail

printf 'Buscando modelos de referencia...\n'
find docs assets -maxdepth 4 -type f 2>/dev/null | sed 's#^./##' | sort || true
