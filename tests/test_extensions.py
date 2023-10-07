from anunnaki_server.app import app

from quart.typing import TestClientProtocol

import logging


async def test_extensions_online_list(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/')
    assert response.status_code == 200
    assert (await response.json)

# async def test_get_extension_by_id(init_app) -> None:
#     client: TestClientProtocol = init_app.test_client()
#     response = await client.get('/extensions/6766468217767473')
#     assert response.status_code == 200
#     data = await response.json
#     assert data['id'] == 6766468217767473

async def test_extension_install(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/')
    assert response.status_code == 200
    data = await response.json
    op_resp = await client.post('/extensions/?operation=install', json=data[0])
    assert op_resp.status_code == 200
    
    installed_response = await client.get('/extensions/?installed=true')
    assert installed_response.status_code == 200
    installed_list = await installed_response.json
    assert installed_list

async def test_extension_update(setup_fake_repos, init_app) -> None:
    default_repo, repo_with_update = setup_fake_repos
    
    client: TestClientProtocol = init_app.test_client()
    ext_response = await client.get('/extensions/')
    data = await ext_response.json
    ext = data[0]
    await client.post('/extensions/?operation=install', json=ext)

    app.config['REPO'] = repo_with_update
    ext['version'] = "1111.0.0"
    op_resp = await client.post('/extensions/?operation=update', json=ext)
    assert op_resp.status_code == 200

    app.config['REPO'] = default_repo
    installed_response = await client.get('/extensions/?installed=true')
    installed_list = await installed_response.json
    assert installed_list[0]['version'] == "1111.0.0"
    
async def test_extension_uninstall(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    ext_response = await client.get('/extensions/')
    data = await ext_response.json
    ext = data[0]
    await client.post('/extensions/?operation=install', json=ext)
    
    op_resp = await client.post('/extensions/?operation=uninstall', json=ext)
    assert op_resp.status_code == 200
    installed_response = await client.get('/extensions/?installed=true')
    installed_list = await installed_response.json
    assert not installed_list

async def test_extensions_filter_installed(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/?installed=true')
    assert response.status_code == 200
    data = await response.json
    assert not data

async def test_extensions_filter_uninstalled(init_app) -> None: 
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/?installed=false')
    assert response.status_code == 200
    data = await response.json
    assert data

async def test_extensions_filter_by_language(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/?lang=ar')
    assert response.status_code == 200
    data = await response.json
    assert data

async def test_extensions_filter_by_name(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/?name=cinemana')
    assert response.status_code == 200
    data = await response.json
    assert len(data) == 2

async def test_extensions_filter_by_has_update_none(init_app) -> None:
    client: TestClientProtocol = init_app.test_client()
    response = await client.get('/extensions/?has_update=true')
    assert response.status_code == 200
    data = await response.json
    assert not data

async def test_extensions_filter_by_has_update_after_install(setup_fake_repos, init_app) -> None:
    _, repo_with_update = setup_fake_repos
    client: TestClientProtocol = init_app.test_client()
   
    ext_response = await client.get('/extensions/')
    data = await ext_response.json
    for ext in data:
        resp = await client.post('/extensions/?operation=install', json=ext)
        assert resp.status_code == 200

    response = await client.get('/extensions/?installed=false')
    assert response.status_code == 200
    data = await response.json
    assert not data

    app.config['REPO'] = repo_with_update
    response = await client.get('/extensions/?has_update=true')
    assert response.status_code == 200
    data = await response.json
    assert len(data) == 1

    response = await client.get('/extensions/?has_update=false')
    assert response.status_code == 200
    data = await response.json
    assert len(data) == 1

    response = await client.get('/extensions/?lang=ar&has_update=false')
    assert response.status_code == 200
    data = await response.json
    assert len(data) == 1
    