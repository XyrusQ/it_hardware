def test_get_employees_list(client):
    response = client.get('/employees/')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_post_employees_list(client):
    response = client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    assert response.status_code == 200
    assert isinstance(response.json, dict)

    response = client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    assert response.status_code == 400


def test_get_employee(client):
    response = client.get('/employees/1')
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    response = client.get('/employees/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_delete_employee(client):
    response = client.delete('/employees/1')
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    client.post('/hardware/', data={'name': 'test', 'category': 'test'})
    client.post('/hardware/1/used', data={'employee_id': 1})
    response = client.delete('/employees/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_put_employee(client):
    response = client.put('/employees/1')
    assert response.status_code == 400

    response = client.put('/employees/1', data={'first_name': 'new_test'})
    assert response.status_code == 404

    client.post('/employees/', data={'first_name': 'test', 'second_name': 'test', 'username': 'test'})
    response = client.put('/employees/1', data={'first_name': 'new_test', 'second_name': 'new_test', 'username': 'new_test'})
    assert response.status_code == 200
    assert isinstance(response.json, dict)

    client.post('/employees/', data={'first_name': 'test2', 'second_name': 'test2', 'username': 'test2'})
    response = client.put('/employees/2', data={'username': 'new_test'})
    assert response.status_code == 400
