#!/data/data/com.termux/files/usr/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOPIC_FILE="$HOME/.ntfy_topic"
DEFAULT_TOPIC="https://ntfy.sh/m82-charallave-l4"
TOPIC="${NTFY_TOPIC:-$(cat $TOPIC_FILE 2>/dev/null || echo $DEFAULT_TOPIC)}"
LOG="$SCRIPT_DIR/logs/ntfy.log"
MSG="$1"
[ -z "$MSG" ] && exit 0
printf "%s" "$MSG" | cut -c1-180 | curl -s -o /dev/null -d @- "$TOPIC" -H "Title: M82 LSEG" -H "Priority: high" -H "Tags: rotating_light"
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') NTFY OK: $MSG" >> "$LOG"
