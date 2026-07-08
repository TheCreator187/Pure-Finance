#!/bin/bash
# Run on the server (SSH) to create the CRM inbox for prequalification leads.
set -euo pipefail
ROOT="${1:-/var/www/Pure-Finance}"
INBOX="$ROOT/submissions/prequalification"
mkdir -p "$INBOX/leads"
touch "$INBOX/index.jsonl"
chown -R www-data:www-data "$ROOT/submissions" 2>/dev/null || true
chmod -R 750 "$ROOT/submissions"
chmod 640 "$INBOX/index.jsonl" 2>/dev/null || true
echo "CRM inbox ready: $INBOX"
echo "Point aminaspeace.com CRM to read: $INBOX/index.jsonl and $INBOX/leads/"
