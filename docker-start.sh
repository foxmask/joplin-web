#!/bin/bash
set -eu
joplin --profile /data server start &

echo "joplin-web available at ${JW_FULL_URL}"
sed -i "s,http://0.0.0.0:8001/,${JW_FULL_URL},g" /app/joplin-web/joplin-web/joplin_web/templates/index.html
export JW_BASE="/app"
cd "${JW_BASE}/joplin-web/joplin-web/joplin_web" \
  && source "../../bin/activate" \
  && python app.py

