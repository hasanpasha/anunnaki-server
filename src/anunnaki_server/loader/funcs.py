from quart import current_app

from anunnaki_server.model import Extension 
from anunnaki_server.ext_manager import db
from anunnaki_server.loader.source_manager import SourceManager

import sys
import importlib


def get_extension_by_id(id: int) -> Extension:
    extensions = db.extensions_list()
    for ext in extensions:
        if ext.id == id:
            return ext

async def source_load(ext: Extension) -> SourceManager:
    extensions_path = current_app.config.get("EXTENSIONS")
    if extensions_path not in sys.path:
        sys.path.append(extensions_path)
    
    ext_mod_path = f"{ext.lang}.{ext.pkg}"
    try:
        module = importlib.import_module(ext_mod_path)
        klass = module.load_extension()
        # init sessions
        await klass.init_session()
    except:
        return None
    else:
        return SourceManager(name=ext.name, id=ext.id, type=type(klass), klass=klass)

async def source_load_by_id(id: int) -> SourceManager:
    ext = get_extension_by_id(id)
    if ext is None:
        return None
    
    return await source_load(ext)
    