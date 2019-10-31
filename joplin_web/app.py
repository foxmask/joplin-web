# coding: utf-8
"""
   joplin-web sauce starlette
"""
# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# uvicorn
import uvicorn

from joplin_api import JoplinApi

templates = Jinja2Templates(directory="templates")

# load configuration
settings = Config('.env')


main_app = Starlette()
main_app.debug = settings('JW_DEBUG')

joplin = JoplinApi(token=settings('JOPLIN_WEBCLIPPER_TOKEN'))


async def tag_for_notes(data):
    """
    alter the original data to add the tag related to the note
    :param data:
    :return:
    """
    payload = []
    for note in data.json():
        tag = await joplin.get_notes_tags(note['id'])
        new_note = note
        new_note['tag'] = tag.json() if tag else ''
        payload.append(new_note)
    return payload


async def paginator(request, res):
    """
    paginator to limit the flow of the data to render
    :param request:
    :param res:
    :return:
    """
    note_per_page = settings('JW_PAGINATOR', cast=int, default=20)
    page = int(request.query_params['page']) if 'page' in request.query_params else 0
    start = 0
    end = note_per_page
    if page > 0:
        start = note_per_page * page
        end = note_per_page * (page + 1)
    if len(res.json()) >= end:
        payload = res.json()[start:end]
    else:
        if page == 0:
            payload = res.json()[0:len(res.json())]
        else:
            payload = res.json()[note_per_page * (page - 1):note_per_page * page]

    # get the tag of each note
    tags_list = []
    payload_with_tags = []
    for line in payload:
        tags = await joplin.get_notes_tags(line['id'])
        if tags.json():
            tags_list = []
            for tag in tags.json():
                tags_list.append({'id': tag['id'], 'title': tag['title']})
        if len(tags_list) > 0:
            line['tags'] = tags_list
        payload_with_tags.append(line)
    return payload_with_tags


async def home(request):
    """
        homepage
    """
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

"""
    get stuff : folders, notes, tags
"""


async def nb_notes_by_folder(folders):
    """
    get the number of notes in each folder
    :param folders: folders list
    :return:
    """
    data = []
    # get the number of notes of each folder, if any
    for folder in folders:
        nb_notes = 0
        res_folders_notes = await joplin.get_folders_notes(folder['id'])
        if len(res_folders_notes.json()):
            nb_notes = len(res_folders_notes.json())
        item = folder
        item['nb_notes'] = nb_notes
        if 'children' in folder:
            children = await nb_notes_by_folder(folder['children'])
            item['children'] = children
        data.append(item)
    return data


async def nb_notes_by_tag(tags):
    """
    get the number of notes in each tag
    :param tags: tags list
    :return:
    """
    data = []
    # get the number of notes of each tag, if any
    for tag in tags:
        nb_notes = 0
        res_tags_notes = await joplin.get_tags_notes(tag['id'])
        if len(res_tags_notes.json()):
            nb_notes = len(res_tags_notes.json())
        item = tag
        item['nb_notes'] = nb_notes
        data.append(item)
    return data


async def get_folders(request):
    """
    all the folders
    :param request:
    :return:
    """
    res = await joplin.get_folders()
    data = await nb_notes_by_folder(res.json())
    return JSONResponse(data)


async def get_notes(request):
    """
    all the notes
    :param request:
    :return:
    """
    res = await joplin.get_notes()
    payload = await tag_for_notes(res)
    return JSONResponse(payload)


async def get_tags(request):
    """
    all the tags
    :param request:
    :return:
    """
    res = await joplin.get_tags()
    data = await nb_notes_by_tag(res.json())
    return JSONResponse(data)


async def get_notesbyfolder(request):
    """
    get the notes of the given folder
    :param request:
    :return:
    """
    folder = request.path_params['folder']
    res = await joplin.get_folders_notes(folder)
    # payload = await paginator(request, res)
    payload = await tag_for_notes(res)
    return JSONResponse(payload)


async def get_notesbytag(request):
    """
    get the all the notes related to the tag id
    :param request:
    :return:
    """
    tag_id = request.path_params['tag_id']
    res = await joplin.get_tags_notes(tag_id)
    payload = []
    for note in res.json():
        tag = await joplin.get_notes_tags(note['id'])
        new_note = note
        new_note['tag'] = tag.json() if tag else ''
        payload.append(new_note)
    # return JSONResponse(res.json())
    return JSONResponse(payload)


async def get_note(request):
    """
    get one note by its id
    :param request:
    :return:
    """
    note_id = request.path_params['note_id']
    res = await joplin.get_note(note_id)
    return JSONResponse(res.json())


async def get_notes_tags(request):
    """
    get the tags related to the note id
    :param request:
    :return:
    """
    note_id = request.path_params['note_id']
    res = await joplin.get_notes_tags(note_id)
    return JSONResponse(res.json())


async def get_resource(request):
    """
    get one resource by its id
    :param request:
    :return:
    """
    resource_id = request.path_params['resource_id']
    res = await joplin.get_resource(resource_id)
    return JSONResponse(res.json())


async def get_notes_resources(request):
    """
    get the resources related to the note id
    :param request:
    :return:
    """
    note_id = request.path_params['note_id']
    res = await joplin.get_notes_resources(note_id)
    return JSONResponse(res.json())

"""
    create/update/delete stuff : note, folder, tag
"""


# create note
async def create_notes(request):
    payload = await request.json()
    title = payload['title']
    body = payload['body']
    parent_id = payload['parent_id']
    res = await joplin.create_note(title=title, body=body, parent_id=parent_id)
    return JSONResponse(res.json())


# Update note
async def update_note(request):
    note_id = request.path_params['note_id']
    payload = await request.json()
    title = payload['title']
    body = payload['body']
    parent_id = payload['parent_id']
    res = await joplin.update_note(note_id=note_id, title=title, body=body, parent_id=parent_id)
    return JSONResponse(res.json())


# Delete note
async def delete_note(request):
    note_id = request.path_params['note_id']
    res = await joplin.delete_note(note_id)
    data = {}
    if res.status_code == 200:
        data = {'MSG': 'OK'}
    return JSONResponse(data)


# create folder
async def create_folder(request):
    folder = await request.json()
    res = await joplin.create_folder(folder=folder['title'])
    return JSONResponse(res.json())


# create tag
async def create_tag(request):
    tag = await request.json()
    res = await joplin.create_tag(title=tag['title'])
    return JSONResponse(res.json())


# HTTP Requests
# Error Pages
@main_app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@main_app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)

# The API Routes
api = Router(routes=[
    Mount('/jw', app=Router([
        Route('/tags/', endpoint=get_tags, methods=['GET']),
        Route('/tags/', endpoint=create_tag, methods=['POST']),
        Route('/folders/', endpoint=get_folders, methods=['GET']),
        Route('/folders/', endpoint=create_folder, methods=['POST']),
        Mount('/resources', app=Router([
            Route('/{resource_id}', endpoint=get_resource, methods=['GET'])
        ])),
        Mount('/notes', app=Router([
            Route('/', endpoint=get_notes, methods=['GET']),
            Route('/', endpoint=create_notes, methods=['POST']),
            Route('/{note_id}', endpoint=get_note, methods=['GET']),
            Route('/{note_id}', endpoint=update_note, methods=['PATCH']),
            Route('/{note_id}', endpoint=delete_note, methods=['DELETE']),
            Route('/{note_id}/tags/', endpoint=get_notes_tags, methods=['GET']),
            Route('/{note_id}/resources/', endpoint=get_notes_resources, methods=['GET']),
            Route('/folder/{folder}', endpoint=get_notesbyfolder, methods=['GET']),
            Route('/tag/{tag_id}', endpoint=get_notesbytag, methods=['GET']),
        ]))
    ]))
])

# The Routes to static content and main page
frontend = Router(routes=[
    Route('/', endpoint=home, methods=['GET']),
    Mount('/files', StaticFiles(directory=settings('JOPLIN_RESOURCES'))),
    Mount('/static/css', StaticFiles(directory="static/css")),
    Mount('/static/js', StaticFiles(directory="static/js")),
])

# let's mount each Route
main_app.mount('/api', app=api)
main_app.mount('/', app=frontend)

# Bootstrap
if __name__ == '__main__':
    print('Joplin Web - Starlette powered')
    uvicorn.run(main_app, host='0.0.0.0', port=settings('JW_HTTP_PORT', cast=int, default=8001))
