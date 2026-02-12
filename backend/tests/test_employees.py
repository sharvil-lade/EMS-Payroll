from fastapi.testclient import TestClient

# Test: Create Employee
def test_create_employee(client: TestClient):
    response = client.post(
        "/employees/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "department": "Engineering",
            "role": "Developer",
            "hourly_rate": 50.0,
            "overtime_rate": 75.0,
            "is_active": True
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


# Test: Read All Employees
def test_read_employees(client: TestClient):

    client.post(
        "/employees/",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "department": "HR",
            "role": "Manager",
            "hourly_rate": 60.0,
            "overtime_rate": 90.0,
        },
    )

    response = client.get("/employees/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["email"] == "jane@example.com"


# Test: Read Employee By ID
def test_read_employee_by_id(client: TestClient):

    create_res = client.post(
        "/employees/",
        json={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "department": "Sales",
            "role": "Associate",
            "hourly_rate": 40.0,
            "overtime_rate": 60.0,
        },
    )

    employee_id = create_res.json()["id"]

    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Alice Smith"
    assert data["id"] == employee_id


# Test: Update Employee
def test_update_employee(client: TestClient):

    create_res = client.post(
        "/employees/",
        json={
            "name": "Bob Brown",
            "email": "bob@example.com",
            "department": "IT",
            "role": "Support",
            "hourly_rate": 30.0,
            "overtime_rate": 45.0,
        },
    )

    employee_id = create_res.json()["id"]

    response = client.put(
        f"/employees/{employee_id}",
        json={
            "name": "Bob Brown Updated",
            "email": "bob@example.com",
            "department": "IT",
            "role": "Senior Support",
            "hourly_rate": 35.0,
            "overtime_rate": 52.5,
            "is_active": True
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Bob Brown Updated"
    assert data["hourly_rate"] == 35.0


# Test: Delete Employee
def test_delete_employee(client: TestClient):

    create_res = client.post(
        "/employees/",
        json={
            "name": "Charlie Black",
            "email": "charlie@example.com",
            "department": "Finance",
            "role": "Analyst",
            "hourly_rate": 55.0,
            "overtime_rate": 82.5,
        },
    )

    employee_id = create_res.json()["id"]

    del_res = client.delete(f"/employees/{employee_id}")
    assert del_res.status_code == 200

    # Ensure deleted
    get_res = client.get(f"/employees/{employee_id}")
    assert get_res.status_code == 404
