def test_api_key(app, client):
    response = client.get('/employees/')
    assert response.status_code == 200

    response = client.get('/employees/', headers={'X-API-KEY': 'WRONG_KEY'})
    assert response.status_code == 401
