from fastapi.testclient import TestClient

def test_attendance_flow(client: TestClient):

    #Create Employee
    create_res = client.post("/employees/", json={
        "name": "David Green",
        "email": "david@example.com",
        "department": "Ops",
        "role": "Operator",
        "hourly_rate": 20.0,
        "overtime_rate": 30.0,
    })

    employee_id = create_res.json()["id"]

    #Login
    login_res = client.post(f"/attendance/login/{employee_id}")
    assert login_res.status_code == 200

    login_data = login_res.json()
    assert login_data["employee_id"] == employee_id
    assert login_data["login_time"] is not None
    assert login_data["logout_time"] is None

    #Login Again (Should Fail)
    login_again_res = client.post(f"/attendance/login/{employee_id}")
    assert login_again_res.status_code == 400
    assert "already checked in" in login_again_res.json()["detail"]

    #Logout
    logout_res = client.post(f"/attendance/logout/{employee_id}")
    assert logout_res.status_code == 200

    logout_data = logout_res.json()
    assert logout_data["logout_time"] is not None
    assert logout_data["total_hours"] >= 0.0

    #Logout Again (Should Fail)
    logout_again_res = client.post(f"/attendance/logout/{employee_id}")
    assert logout_again_res.status_code == 400
    assert "No active check-in" in logout_again_res.json()["detail"]


def test_attendance_invalid_employee(client: TestClient):
    res = client.post("/attendance/login/99999")
    assert res.status_code == 404
