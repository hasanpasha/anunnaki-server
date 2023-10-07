from quart import request, abort

from anunnaki_server.model import Extension, Result
from anunnaki_server.loader.funcs import source_load_by_id



async def source_method(id: int, method_name: str):
    data = await request.get_data()

    source_info = await source_load_by_id(id)
    if source_info is None:
        abort(400)

    try:
        result = await source_info.call_method(method_name, data)
    except Exception as e:
        return Result(success=False, error=str(e)), 400
    else:
        return result