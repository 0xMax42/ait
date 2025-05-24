#!/usr/bin/env bash
set -euo pipefail

# Eingabeparameter
FILE_PATH="$1"                      # z. B. ./dist/build.zip
CUSTOM_NAME="${2:-}"               # optional: anderer Name unter dem das Asset gespeichert werden soll
RELEASE_ID="${GT_RELEASE_ID:-}"       # aus Umgebung

# Validierung
if [[ -z "$RELEASE_ID" ]]; then
  echo "❌ RELEASE_ID ist nicht gesetzt. Abbruch."
  exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
  echo "❌ Datei '$FILE_PATH' existiert nicht. Abbruch."
  exit 1
fi

# Default-Konfiguration
TOKEN="${ACTIONS_RUNTIME_TOKEN:-<fallback_token>}"
REPO="${GITHUB_REPOSITORY:-owner/example}"
API="${GITHUB_API_URL:-https://gitea.example.tld/api/v1}"

# Owner/Repo auflösen
OWNER=$(echo "$REPO" | cut -d/ -f1)
NAME=$(echo "$REPO" | cut -d/ -f2)

# Dateiname setzen
FILENAME="${CUSTOM_NAME:-$(basename "$FILE_PATH")}"

echo "🔼 Uploading '$FILE_PATH' as '$FILENAME' to release ID $RELEASE_ID"

# Upload
curl -sf -X POST \
  -H "Authorization: token $TOKEN" \
  -F "attachment=@$FILE_PATH" \
  "$API/repos/$OWNER/$NAME/releases/$RELEASE_ID/assets?name=$FILENAME"

echo "✅ Upload abgeschlossen: $FILENAME"
