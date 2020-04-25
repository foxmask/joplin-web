# Docker

if you prefer to run the project from docker follow that steps:

## before building 

### set the environment
`cp joplin_web/env.docker.sample .env`
Copy the example env and do not forget to setup the parms in the `.env` file describes in the `settings` paragraph of the [README.md](README.md#settings). At least the joplin webclipper token needs to be set.

### get the joplin config directory

Configure your joplin app like you want it. Afterwards copy your joplin config directory to the directory where you want to mount the docker volume.

`cp -r /home/foxmask/.config/joplin-desktop /data/`

### define the URL to joplin web

Think about the full URL where you want your joplin web app to be accessible. If you want to access it at the default URL `http://127.0.0.1:8001/` no separate definition is needed.

If you want to change the URL, it is important that your URL ends with a slash.

## build the docker image by

```
docker build -t joplin-web-build . 
```

## run the image
```
docker run -p 8001:8001 -v /data/joplin-desktop:/data -e JW_FULL_URL="http://192.168.0.3:8001/" joplin-web-build
joplin-web available at http://192.168.0.3:8001/
/
Joplin Web Companion - Starlette powered
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
23:44:39
INFO:     192.168.0.2:33462 - "GET / HTTP/1.1" 200 OK
```
