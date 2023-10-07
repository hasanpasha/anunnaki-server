from anunnaki_server.app import app, init_db
from anunnaki_server.ext_manager.repo import Repo

import pytest
import time
import multiprocessing
from http.server import HTTPServer, SimpleHTTPRequestHandler


class DefaultHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, *, directory: str = None) -> None:
        super().__init__(request, client_address, server, directory="tests/fake_data/fake_data_no_update")

class DefaultHandlerWithUpdate(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, *, directory: str = None) -> None:
        super().__init__(request, client_address, server, directory="tests/fake_data/fake_data_with_update")


@pytest.fixture(autouse=True)
async def init_app(tmpdir):
    app.config['DATABASE'] = str(tmpdir.join('data.db'))
    app.config['EXTENSIONS'] = str(tmpdir.join('extensions'))
    init_db()
    async with app.test_app() as test_app:
        yield test_app

@pytest.fixture(autouse=True, scope="session")
def setup_fake_repos():
    ports = [8080, 8081]
    servers = [
        HTTPServer(('localhost', ports[0]), DefaultHandler),
        HTTPServer(('localhost', ports[1]), DefaultHandlerWithUpdate),
    ]
    
    default_repo = Repo(url=f"http://localhost:{ports[0]}", index_file="index.json")
    repo_with_update = Repo(url=f"http://localhost:{ports[1]}", index_file="index.json")
    
    procs = [multiprocessing.Process(target=server.serve_forever) for server in servers]

    # Start procs
    for proc in procs:
        proc.start()

    time.sleep(1)

    # Set default repo
    app.config["REPO"] = default_repo

    yield default_repo, repo_with_update

    for proc in procs:
        proc.terminate()