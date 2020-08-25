#!/bin/bash
set -eu
joplin --profile /data server start &
# the if checks if JW_SYNC_SECONDS is a number, if yes sync joplin data after sleeping that amount of seconds
(
  if [ -n "$JW_SYNC_SECONDS"  ] && [ "$JW_SYNC_SECONDS" -eq "$JW_SYNC_SECONDS"  ] 2>/dev/null;
  then
    while true
    do
      echo "sleeping for $JW_SYNC_SECONDS seconds before the next joplin sync"
      sleep "$JW_SYNC_SECONDS"
      joplin --profile /data sync
    done
  fi
) &

echo "joplin-web available at ${JW_FULL_URL}"
sed -i "s,http://0.0.0.0:8001/,${JW_FULL_URL},g" /app/joplin-web/joplin-web/joplin_web/templates/index.html
export JW_BASE="/app"
cd "${JW_BASE}/joplin-web/joplin-web/joplin_web" \
  && source "../../bin/activate" \
  && python app.py

