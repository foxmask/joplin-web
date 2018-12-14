# Joplin Web : The BackEnd

A Web application for [Joplin](https://joplin.cozic.net/)

## why that project ?

Because it may happened we need to access to [Joplin](https://joplin.cozic.net/) without having access to his/her smartphone or the Joplin Desktop, and a Web Application could to the trick at a given moment.

## Requirements

* Python >= 3.6
* [Joplin-API](https://github.com/foxmask/joplin-api)
* [Django Rest Framework](http://www.django-rest-framework.org/#installation)
* django-environ
* requests

## Installation 

```python
python3 -m venv joplin-web
cd joplin-web
source bin/activate
git clone https://github.com/foxmask/joplin-web
cd joplin-web
pip install -r requirements-dev.txt
```

### settings 

copy env.sample to .env

then set : 

* the `JOPLIN_PATH` to the database 
* the `JOPLIN_TOKEN` you have in the Webclipper config page in Joplin


If you plan to use joplin-terminal and not the WebClipper, in your `.env` file, set `API_USE_JOPLIN_WEBCLIPPER` to `False` then joplin-web will switch of API calls from Rest to command line.


#### Database

```python
python manage.py migrate
```

this will add the tables of django but will not change any joplin tables

### Running

```python
python manage.py runserver localhost:8001 &
```
if you map another port, you will need to have a look at the front end `vue.config.js` file

Now proceed with setting up the frontend.

# Joplin-front : The Frontend

see [`joplin-web/joplin-front/README.md`](joplin-front/README.md) file

![Joplin web](https://raw.githubusercontent.com/foxmask/joplin-web/master/joplin_web.png)
