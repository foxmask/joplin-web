FROM python:3.6
ENV PYTHONUNBUFFERED=1 \
    JW_FULL_URL="http://127.0.0.1:8001/"
WORKDIR  /app
COPY requirements.txt /app/
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
  && apt-get install nodejs \
  && NPM_CONFIG_PREFIX=/joplin-bin npm install --unsafe-perm -g joplin \
  && ln -s /joplin-bin/bin/joplin /usr/bin/joplin \
  && pip install -r requirements.txt \
  && mkdir /data
COPY joplin_web /app
COPY docker-start.sh /app/
COPY .env /app/

VOLUME /data
EXPOSE 8001
CMD ["/app/docker-start.sh"]
