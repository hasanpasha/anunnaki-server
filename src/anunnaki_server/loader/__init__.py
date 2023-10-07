from quart import Blueprint, request, abort
# from anunnaki_server.loader import views

from anunnaki_server.ext_manager import db
from anunnaki_server.model import Extension

from anunnaki_server.loader.funcs import extension_load

import asyncio

loader_blueprint = Blueprint('loader_blueprint', __name__)


def get_extension_by_id(id: int) -> Extension:
    extensions = db.extensions_list()
    for ext in extensions:
        if ext.id == id:
            return ext
        

async def index(id: int):
    try:
        id = int(id)
    except:
        abort(400)
    
    ext = get_extension_by_id(id)
    if ext is None:
        abort(404)
        
    # r = repr(ext)
    # return f"THE EXTENSION {r} {}"
    source = await extension_load(ext)
    await source.init_session()
    resp = await source.fetch_search_media("the day after", 1)
    await source.session.close()
    return repr(resp.medias)

async def source_method(id: int, method: str):
    ext = get_extension_by_id(id)
    if ext is None:
        abort(404)

    args = request.args.to_dict()
    
    source = await extension_load(ext)
    await source.init_session()
    resp = await source.fetch_search_media("the day after", 1)
    await source.session.close()
    return repr(resp.medias)


# async def get_name(id):
#     args = repr(request.args.to_dict())

#     return f"NAME {id} {args}"

loader_blueprint.add_url_rule('/', 'index', view_func=index)
loader_blueprint.add_url_rule('/<string:method>/', view_func=source_method)
# loader_blueprint.add_url_rule('/get_name', 'get_name', view_func=get_name)