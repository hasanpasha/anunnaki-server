from anunnaki_server.app import app

async def test_index() -> None:
    test_client = app.test_client()
    response = await test_client.get('/')
    assert response.status_code == 200
    data = await response.get_data(as_text=True)
    assert data == "Hello, World!"
    