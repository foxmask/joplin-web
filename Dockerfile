FROM python:3.8-buster
SHELL ["/bin/bash", "-c"]
ENV PYTHONUNBUFFERED=1 \
    JW_FULL_URL="http://127.0.0.1:8001/" \
    JW_SYNC_SECONDS=300
WORKDIR /app
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y libsecret-1-dev nodejs \
  && NPM_CONFIG_PREFIX=/joplin-bin npm install --unsafe-perm -g joplin \
  && ln -s /joplin-bin/bin/joplin /usr/bin/joplin \
  && export JW_BASE=/app \
  && cd "${JW_BASE}" \
  && python3 -m venv joplin-web \
  && cd joplin-web \
  && source bin/activate \
  && git clone https://github.com/foxmask/joplin-web \
  && cd joplin-web \
  && pip install -r requirements.txt \
  && cd joplin-vue \
  && npm install \
  && npm run build \
  && mkdir /data

VOLUME /data
EXPOSE 8001
COPY .env /app/joplin-web/joplin-web/joplin_web/
CMD ["/app/joplin-web/joplin-web/docker-start.sh"]
