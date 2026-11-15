def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == [{"name": "Aarav", "salary": 55000}]


def test_get_employee_success(client):
    response = client.get("/employees/Aarav")
    assert response.status_code == 200
    assert response.json()["name"] == "Aarav"


def test_get_employee_not_found(client):
    response = client.get("/employees/Ravi")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_employee_success(client):
    response = client.post(
        "/employees", json={"name": "Ravi", "salary": 70000}
    )
    assert response.status_code == 201
    assert response.json() == {"name": "Ravi", "salary": 70000}


def test_invalid_salary(client):
    response = client.post(
        "/employees", json={"name": "Ravi", "salary": -5}
    )
    assert response.status_code == 422


def test_empty_name(client):
    response = client.post(
        "/employees", json={"name": "   ", "salary": 50000}
    )
    assert response.status_code == 422


def test_zero_salary(client):
    response = client.post(
        "/employees", json={"name": "Ravi", "salary": 0}
    )
    assert response.status_code == 422
