#!/usr/bin/env bash
set -euo pipefail

# cleanup_dev_versions.sh - Delete old PyPI dev versions from Gitea package registry

# Required environment variables
USERNAME="${TWINE_USERNAME}"
TOKEN="${TWINE_PASSWORD}"
REPO="${GITHUB_REPOSITORY}"             # e.g., maxp/repocat
API_BASE="${GITHUB_API_URL%/}"         # Strip trailing slash if present

OWNER="${REPO%%/*}"
PACKAGE_NAME="${REPO##*/}"
API_URL="${API_BASE}/packages/${OWNER}/pypi/${PACKAGE_NAME}"

# Fetch the list of versions
response=$(curl -s -u "$USERNAME:$TOKEN" "$API_URL")

# Extract all .dev versions, sort by creation time
mapfile -t versions_to_delete < <(echo "$response" | jq -r '
  map(select(.version | test("\\.dev"))) |
  sort_by(.created_at) |
  .[0:-1][] |
  .version')

# Determine latest version to keep
latest_version=$(echo "$response" | jq -r '
  map(select(.version | test("\\.dev"))) |
  sort_by(.created_at) |
  last.version')

if [[ -z "$latest_version" || ${#versions_to_delete[@]} -eq 0 ]]; then
  echo "No old .dev versions to delete."
  exit 0
fi

echo "Keeping latest .dev version: $latest_version"

# Delete old .dev versions
for version in "${versions_to_delete[@]}"; do
  echo "Deleting old .dev version: $version"
  curl -s -X DELETE -u "$USERNAME:$TOKEN" "$API_URL/$version"
done

echo "Cleanup complete."