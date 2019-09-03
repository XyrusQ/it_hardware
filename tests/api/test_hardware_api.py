def test_get_hardware_list(client):
    response = client.get('/hardware/')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_post_hardware_list(client):
    response = client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_get_hardware(client):
    response = client.get('/hardware/1')
    assert response.status_code == 404

    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    response = client.get('/hardware/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_delete_hardware(client):
    response = client.delete('/hardware/1')
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    client.post('/hardware/1/used', data={'employee_id': 1})
    response = client.delete('/hardware/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_get_used_hardware(client):
    response = client.get('/hardware/1/used')
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    client.post('/hardware/1/used', data={'employee_id': 1})
    response = client.get('/hardware/1/used')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_post_used_hardware(client):
    response = client.post('/hardware/1/used')
    assert response.status_code == 400

    response = client.post('/hardware/1/used', data={'employee_id': 1})
    assert response.status_code == 400

    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    response = client.post('/hardware/1/used', data={'employee_id': 1})
    assert response.status_code == 400

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    response = client.post('/hardware/1/used', data={'employee_id': 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)

    client.post('/employees/', data={'first_name': 'test2', 'second_name': 'test2', 'username': 'test2'})
    response = client.post('/hardware/1/used', data={'employee_id': 2})
    assert response.status_code == 400


def test_delete_used_hardware(client):
    response = client.delete('/hardware/1/used')
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    client.post('/hardware/1/used', data={'employee_id': 1})

    response = client.delete('/hardware/1/used')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_put_used_hardware(client):
    response = client.put('/hardware/1/used')
    assert response.status_code == 400

    response = client.put('/hardware/1/used', data={'employee_id': 1})
    assert response.status_code == 400

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    response = client.put('/hardware/1/used', data={'employee_id': 1})
    assert response.status_code == 400

    client.post('/employees/', data={'first_name': 'test2', 'second_name': 'test2', 'username': 'test2'})
    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    client.post('/hardware/1/used', data={'employee_id': 1})
    response = client.put('/hardware/1/used', data={'employee_id': 2})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
