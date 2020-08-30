# Joplin Web
[TOC] 

A Web application companion for [JoplinApp](https://joplinapp.org)

![Joplin web](https://raw.githubusercontent.com/foxmask/joplin-web/master/joplin_web.png)

## Why did we make this project?

We needed to access to [JoplinApp](https://joplinapp.org) without having access to our smartphone or the Joplin Desktop, and so we built a Web version that could give us access from wherever

## Requirements

* Python >= 3.6
* [joplin-api](https://github.com/foxmask/joplin-api)
* [starlette](https://www.starlette.io) (installed as part of Python resources)
* [VueJS](https://vuejs.org)

---

## Installation

```python
export JW_BASE="${HOME}" # Set the directory where you would like to install
cd "${JW_BASE}"
python3 -m venv joplin-web
cd joplin-web
source bin/activate
git clone https://github.com/foxmask/joplin-web
cd joplin-web
pip install -r requirements.txt
cd joplin-vue
npm install
```

### Set Environment Parameters
In `${JW_BASE}/joplin-web/joplin-web/joplin-web`, copy `env.sample` to `.env`:

Required parameters:
* `JOPLIN_WEBCLIPPER_TOKEN`: From the Joplin Desktop app, go to Settings > Web Clipper to enable Web Clipper and find your token
* `JOPLIN_RESOURCES`: The resources in Joplin Web are from the Desktop app resource directory
* `JW_BASE_URL`: If you want to install Joplin Web in a subdirectory, you can update the base. For example, set it to `/joplin/` to move the URL from `/` to  `/joplin/`

Optional paramenters:
* `JW_DEBUG`: You can choose to run the app in debug mode or not
* `JW_PAGINATOR`: Choose the number of notes per page
* `JW_HTTP_PORT`: Set the port number to view the app. For example localhost:8001

### Start a version of Joplin
In order to use the Joplin Web app, you will need to have a version of Joplin running. 

*Option 1:* Joplin Desktop App
* Launch the Joplin Desktop App as normal. Make sure Web Clipper is running, so that the API is available. 

*Option 2:* Joplin Headless
* If you are using joplin on a dedicated server, you can start "joplin headless", as follow
```
joplin --profile ~/.config/joplin-desktop/ server start
Server is already running on port 41184
```
joplin headless is available with the "joplin terminal" version (since build 147), you can install like that
```
NPM_CONFIG_PREFIX=~/.joplin-bin npm install -g joplin
sudo ln -s ~/.joplin-bin/bin/joplin /usr/bin/joplin
```
(have a look at https://joplinapp.org/ for more details)

### Run the App for Normal Use
1. Compile the vuejs project
```shell
cd joplin-vue
npm run build
```

2. Start the application
```python
export JW_BASE="${HOME}" # Must match value used at install time
cd "${JW_BASE}/joplin-web/joplin-web/joplin_web"
source "../../bin/activate"
python app.py &
Joplin Web - Starlette powered
Started server process [11243]
Waiting for application startup.
Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

---

## Starting App for Development

Start the front and the back end in 2 dedicated process

1. Start the backend

```python
export JW_BASE="${HOME}" # Must match value used at install time
cd "${JW_BASE}/joplin-web/joplin-web/joplin_web"
source "../../bin/activate"
python app.py &
Joplin Web - Starlette powered
Started server process [10043]
Waiting for application startup.
Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

2. Start the frontend

see [`joplin-web/joplin-vue/README.md`](joplin-vue/README.md) file

---


# Joplin-web : Docker

if you prefer to run the project from docker:

see [joplin-web/docker.md](docker.md) for details

# System settings

see [joplin-web/system.md](system.md) for details
