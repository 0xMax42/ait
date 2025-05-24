#!/bin/bash

BASE_VERSION=$(cat VERSION)
NIGHTLY_SUFFIX=""

if [[ "$1" == "nightly" ]]; then
  # Beispiel: 20240511.1358 → 11. Mai, 13:58 Uhr
  NIGHTLY_SUFFIX=".dev$(date +%Y%m%d%H%M)"
fi

FULL_VERSION="${BASE_VERSION}${NIGHTLY_SUFFIX}"

echo "Using version: $FULL_VERSION"
poetry version "$FULL_VERSION"
