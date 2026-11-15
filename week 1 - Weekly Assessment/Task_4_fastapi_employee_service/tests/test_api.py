def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Asha"


def test_get_employee_success(client):
    response = client.get("/employees/Rahul")
    assert response.status_code == 200
    assert response.json()["salary"] == 52000


def test_get_employee_not_found(client):
    response = client.get("/employees/Ravi")
    assert response.status_code == 404


def test_create_employee_success(client):
    response = client.post("/employees", json={"name": "Meera", "salary": 70000})
    assert response.status_code == 201
    assert response.json()["name"] == "Meera"
    assert client.get("/employees/Meera").status_code == 200


def test_invalid_salary(client):
    response = client.post("/employees", json={"name": "Amit", "salary": -5})
    assert response.status_code == 422


def test_empty_name(client):
    response = client.post("/employees", json={"name": "   ", "salary": 30000})
    assert response.status_code == 422


def test_duplicate_employee(client):
    response = client.post("/employees", json={"name": "asha", "salary": 30000})
    assert response.status_code == 409
