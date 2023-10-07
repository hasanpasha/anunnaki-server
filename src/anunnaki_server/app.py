from quart import Quart, g
from quart_schema import QuartSchema, validate_response

from anunnaki_server.ext_manager import mn_blueprint
from anunnaki_server.ext_manager.repo import Repo
from anunnaki_server.model import Result
from anunnaki_server.loader import loader_blueprint

import os
import pathlib
from sqlite3 import dbapi2 as sqlite3
import aiohttp

app = Quart(__name__)
app.config.update({
    "DATABASE": os.path.join(app.root_path, 'data/data.sqlite'),
    "EXTENSIONS": os.path.join(app.root_path, 'data/extensions'),
    "REPO": Repo()
})
QuartSchema(app)

app.register_blueprint(mn_blueprint, url_prefix="/extensions")
app.register_blueprint(loader_blueprint, url_prefix="/<int:id>")

def connect_db():
    db_path = app.config.get("DATABASE")
    db_dir = pathlib.Path(db_path).parent
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    engine = sqlite3.connect(db_path)
    engine.row_factory = sqlite3.Row
    return engine

def init_db():
    db = connect_db()
    with open(os.path.join(app.root_path, 'schema.sql'), mode="r") as file_:
        db.cursor().execute(file_.read())
    db.commit()

@app.before_request
async def set_db(): 
    if not hasattr(app, "sqlite_db"):
        g.sqlite_db = connect_db()

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

@app.after_serving
async def teardown():
    await app.client_session.close()

@app.get('/')
async def index():
    return "Hello, World!"