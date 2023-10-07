from quart import current_app

from anunnaki_server.model import Extension 

from anunnaki_source import Source, CatalogueSource
from anunnaki_source.online import HttpSource
import os
import sys
import importlib

async def extension_load(ext: Extension) -> CatalogueSource:
    extensions_path = current_app.config.get("EXTENSIONS")
    if extensions_path not in sys.path:
        sys.path.append(extensions_path)
    
    ext_mod_path = f"{ext.lang}.{ext.pkg}"
    module = importlib.import_module(ext_mod_path)
    klass = module.load_extension()
    return klass