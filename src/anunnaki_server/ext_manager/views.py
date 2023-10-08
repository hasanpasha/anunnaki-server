from quart import request, abort, redirect, url_for
from quart_schema import validate_request, validate_response

from anunnaki_server.model import Extension, ExtensionList, Result
from anunnaki_server.ext_manager import db
from anunnaki_server.ext_manager.funcs import *

from aiohttp import ClientSession



# TODO: add swagger documenting
@validate_response(ExtensionList)
async def extensions_list():
    installed_extensions = await db.extensions_list()
    result_extensions: List[Extension] = None

    args = request.args
    installed_arg: bool = args.get("installed", type=lambda v: v.lower() == "true")
    has_update_arg: bool = args.get("has_update", type=lambda v: v.lower() == "true")
    lang_arg: str = args.get("lang", type=str)
    name_arg: str = args.get("name", type=str)

    if installed_arg is not None:
        if installed_arg:
            result_extensions = installed_extensions
        else:
            marked_exts = await get_extensions_from_repo()
            result_extensions = [ext for ext in marked_exts if not ext.installed]
    else:
        result_extensions = await get_extensions_from_repo()

    if has_update_arg:
        result_extensions = [ext for ext in result_extensions if ext.has_new_update]
    else:
        result_extensions = [ext for ext in result_extensions if not ext.has_new_update]
    
    if lang_arg is not None:
        result_extensions = [ext for ext in result_extensions if ext.lang == lang_arg]

    if name_arg is not None:
        result_extensions = [ext for ext in result_extensions if ext.name == name_arg]

    return ExtensionList(root=result_extensions)

async def select_operation(ext: Extension, args) -> Result:
    operation = args.get("operation")
    if operation is None:
        abort(400)

    if operation == "install":
        return await extension_install(ext)
    elif operation == "uninstall":
        return await extension_uninstall(ext)
    elif operation == "update":
        return await extension_update(ext)
    else:
        abort(405)

@validate_request(Extension)
@validate_response(Result)
async def extension_operation(data: Extension):
    args = request.args
    return await select_operation(data, args)

async def extension_operation_by_id(id: int):
    online_extensions = await get_extensions_from_repo()

    client_session: ClientSession = current_app.client_session

    try:
        id = int(id)
    except:
        abort(506)

    for ext in online_extensions:
        if ext.id == id:
            return await select_operation(ext, request.args)
    else:
        abort(405)