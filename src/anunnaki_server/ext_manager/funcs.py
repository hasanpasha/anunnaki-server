from quart import current_app, abort

from anunnaki_server.model import Extension, Result
from anunnaki_server.ext_manager import db
from anunnaki_server.ext_manager.repo import Repo
from anunnaki_server.utils import delete_folder

from typing import List
from aiohttp import ClientSession
import os
import zipfile
import io
import logging

async def get_extensions_from_repo(repo: Repo = None) -> List[Extension]:
    """
    Download online extensiosn info from the repo
    """
    if repo is None:
        repo: Repo = current_app.config.get("REPO")
    installed_extensions = db.extensions_list()
    
    session: ClientSession = current_app.client_session 
    async with session.get(repo.index_path()) as resp:
        if not resp.ok:
            abort(500)
            
        extensions_json = await resp.json(content_type=resp.content_type)
        extensions = [Extension(**extension) for extension in extensions_json]
        return [extension.mark_extension(installed_extensions) for extension in extensions]

async def download_extension(extension: Extension) -> bool:
    """
    Download the extensions and extract it to the apropriate path
    and report success
    """
    repo: Repo = current_app.config.get("REPO")
    session: ClientSession = current_app.client_session
    async with session.get(repo.zip_url(extension)) as resp:
        if not resp.ok:
            return False
        
        output_path = os.path.join(current_app.config.get("EXTENSIONS"), extension.lang)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        data = await resp.read()
        z = zipfile.ZipFile(io.BytesIO(data))
        z.extractall(os.path.join(output_path, extension.pkg))

    return True

def delete_extension_folder(extension: Extension) -> bool:
    """Remove extension folder"""
    extension_path = os.path.join(current_app.config.get("EXTENSIONS"), extension.lang, extension.pkg)
    return delete_folder(extension_path)

async def extension_install(extension: Extension) -> Result:
    """
    Download the extension and add its data to database table
    """
    repo: Repo = current_app.config.get("REPO")
    session: ClientSession = current_app.client_session
    async with session.get(repo.zip_url(extension)) as resp:
        if not resp.ok:
            logging.error(repo.zip_url(extension))
            abort(500)
        
        if not (await download_extension(extension)):
            abort(501)

        if not db.extension_add(extension):
            abort(502)

        return Result(success=True)
            
async def extension_uninstall(extension: Extension) -> Result:
    """
    Remove the extensions folder and remove its 
    data row from the database table
    """
    if not delete_extension_folder(extension):
        abort(500)

    if not db.extension_remove(extension):
        abort(500)
    
    return Result(success=True)
            
async def extension_update(extension: Extension) -> Result:
    """
    Remove the old extension folder and install the new one 
    then update the database table
    """
    repo: Repo = current_app.config.get("REPO")
    session: ClientSession = current_app.client_session 
    async with session.get(repo.zip_url(extension)) as resp:
        if not resp.ok:
            abort(500)
        
        if not delete_extension_folder(extension):
            abort(500)

        if not (await download_extension(extension)):
            abort(500)

        if not db.extension_update(extension):
            abort(500)

        return Result(success=True)