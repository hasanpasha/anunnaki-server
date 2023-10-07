from quart import request, abort, current_app

from anunnaki_server.model import Result
from anunnaki_server.loader.funcs import source_load_by_id




async def source_method(id: int, method_name: str):
    data = await request.get_data()

    # cache sources
    sources: dict = current_app.config.get("SOURCES")
    if id not in sources.keys():
        source_info = await source_load_by_id(id)
        if source_info is None:
            Result(success=False, error="Error loading source"), 200
        sources[id] = source_info
    else:
        source_info = sources[id]

    try:
        result = await source_info.call_method(method_name, data)
    except Exception as e:
        return Result(success=False, error=str(e)), 200
    else:
        return result