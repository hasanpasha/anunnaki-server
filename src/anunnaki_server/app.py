from quart import Quart, g
from quart_schema import QuartSchema, validate_response

from anunnaki_server.ext_manager import mn_blueprint
from anunnaki_server.loader import loader_blueprint
from anunnaki_server.ext_manager.repo import Repo
from anunnaki_server.model import Result

import os
import pathlib
import aiosqlite
import aiohttp

app = Quart(__name__)
app.config.update({
    "DATABASE": os.path.join(app.root_path, 'data/data.sqlite'),
    "EXTENSIONS": os.path.join(app.root_path, 'data/extensions'),
    "REPO": Repo(),
    "SOURCES": dict(), # Stores SourceManager instances
})
QuartSchema(app)

app.register_blueprint(mn_blueprint, url_prefix="/extensions")
app.register_blueprint(loader_blueprint, url_prefix="/<int:id>")

async def connect_db() -> aiosqlite.Connection:
    db_path = app.config.get("DATABASE")
    db_dir = pathlib.Path(db_path).parent
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    engine = await aiosqlite.connect(db_path)
    engine.row_factory = aiosqlite.Row
    return engine

async def init_db() -> aiosqlite.Connection:
    db = await connect_db()
    with open(os.path.join(app.root_path, 'schema.sql'), mode="r") as file_:
        await db.execute(file_.read())
        await db.commit()
    return db

@app.errorhandler(500)
@validate_response(Result)
async def server_error(error):
    return Result(success=False, error="Server Internal Error"), 500

@app.errorhandler(405)
@validate_response(Result)
async def method_not_allowed(error):
    return Result(success=False, error="Method Not Allowed"), 405

@app.errorhandler(400)
@validate_response(Result)
async def bad_request(error):
    return Result(success=False, error="Bad Request"), 400

@app.before_serving
async def startup():
    app.client_session = aiohttp.ClientSession()
    app.sqlite_db = await init_db()

@app.after_serving
async def teardown():
    await app.client_session.close()
    await app.sqlite_db.close()

@app.get('/')
async def index():
    return "Hello, World!"