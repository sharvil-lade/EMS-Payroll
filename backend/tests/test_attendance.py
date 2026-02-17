from fastapi.testclient import TestClient
from datetime import date

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


    res = client.post("/attendance/login/99999")
    assert res.status_code == 404


# def test_manual_attendance_entry(client: TestClient):
#     # Create employee
#     create_res = client.post("/employees/", json={
#         "name": "Manual Tester",
#         "email": "manual@test.com",
#         "department": "Test",
#         "role": "Tester",
#         "hourly_rate": 20.0,
#         "overtime_rate": 30.0,
#     })
#     employee_id = create_res.json()["id"]

#     # Add manual entry
#     manual_date = "2023-10-25"
#     manual_res = client.post("/attendance/manual", json={
#         "employee_id": employee_id,
#         "date": manual_date,
#         "standard_hours": 8.5,
#         "overtime_hours": 2.5
#     })
#     assert manual_res.status_code == 200
#     data = manual_res.json()
#     assert data["standard_hours"] == 8.5
#     assert data["overtime_hours"] == 2.5

#     # Verify via Report
#     report_res = client.get(f"/attendance/report?employee_id={employee_id}&start_date={manual_date}&end_date={manual_date}")
#     assert report_res.status_code == 200
#     report_data = report_res.json()
#     assert report_data["total_hours"] == 11.0 # 8.5 + 2.5
#     assert report_data["total_standard_hours"] == 8.5
#     assert report_data["total_overtime_hours"] == 2.5
#     assert report_data["daily_breakdown"][0]["total_hours"] == 11.0

# def test_report_priority_manual_over_auto(client: TestClient):
#     # Create employee
#     create_res = client.post("/employees/", json={
#         "name": "Priority Tester",
#         "email": "priority@test.com",
#         "department": "Test",
#         "role": "Tester",
#         "hourly_rate": 20.0,
#         "overtime_rate": 30.0,
#     })
#     employee_id = create_res.json()["id"]
    
#     # 1. Login
#     client.post(f"/attendance/login/{employee_id}")
#     # 2. Logout (will give small duration)
#     client.post(f"/attendance/logout/{employee_id}")
    
#     # Check report - should be near 0 hours
#     today = str(date.today())
#     report_res = client.get(f"/attendance/report?employee_id={employee_id}&start_date={today}&end_date={today}")
#     auto_total = report_res.json()["total_hours"]
#     assert auto_total < 1.0

#     # 3. Add Manual Override for TODAY with 10 hours
#     manual_res = client.post("/attendance/manual", json={
#         "employee_id": employee_id,
#         "date": today,
#         "standard_hours": 8.0,
#         "overtime_hours": 2.0
#     })
#     assert manual_res.status_code == 200

#     # 4. Check Report again - should be 10 hours
#     report_res_2 = client.get(f"/attendance/report?employee_id={employee_id}&start_date={today}&end_date={today}")
#     manual_total = report_res_2.json()["total_hours"]
#     assert manual_total == 10.0
