#!/usr/bin/env bash
set -euo pipefail

# Eingaben
TAG="$1"
TOKEN="${ACTIONS_RUNTIME_TOKEN:-<fallback_token>}"
REPO="${GITHUB_REPOSITORY:-owner/example}"
API="${GITHUB_API_URL:-https://gitea.example.tld/api/v1}"

OWNER=$(echo "$REPO" | cut -d/ -f1)
NAME=$(echo "$REPO" | cut -d/ -f2)

RESPONSE=$(curl -sf \
  -H "Authorization: token $TOKEN" \
  "$API/repos/$OWNER/$NAME/releases/tags/$TAG")

RELEASE_ID=$(echo "$RESPONSE" | jq -r '.id')
echo "Release-ID für $TAG ist: $RELEASE_ID"

# Für GitHub Actions als Umgebungsvariable
echo "GT_RELEASE_ID=$RELEASE_ID" >> "$GITHUB_ENV"
