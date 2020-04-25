#!/bin/bash
set -eu
echo "joplin-web available at ${JW_FULL_URL}"
sed -i "s,http://0.0.0.0:8001/,${JW_FULL_URL},g" /app/templates/index.html
joplin --profile /data server start &
python /app/app.py

