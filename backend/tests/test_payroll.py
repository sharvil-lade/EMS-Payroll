from fastapi.testclient import TestClient
from datetime import date, datetime, timedelta
from app.models.attendance import Attendance

def test_payroll_calculation(client: TestClient, test_db):
    res = client.post("/employees/", json={
        "name": "Payroll Test User",
        "email": "payroll@example.com",
        "department": "Finance",
        "role": "Accountant",
        "hourly_rate": 100.0,
        "overtime_rate": 150.0,
    })

    employee_id = res.json()["id"]

    base_date = date(2026, 2, 2)

    hours_list = [8, 10, 7, 9, 8, 5]

    records = []

    for i in range(6):
        current_date = base_date + timedelta(days=i)
        hours = hours_list[i]

        records.append(
            Attendance(
                employee_id=employee_id,
                date=current_date,
                login_time=datetime.combine(current_date, datetime.min.time()),
                logout_time=datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hours),
                total_hours=float(hours)
            )
        )

    test_db.add_all(records)
    test_db.commit()

    report_res = client.post("/payroll/report", json={
        "employee_id": employee_id,
        "start_date": "2026-02-02",
        "end_date": "2026-02-07"
    })

    assert report_res.status_code == 200
    report = report_res.json()

    expected_standard = 8 + 8 + 7 + 8 + 8   
    expected_overtime = 2 + 1               
    expected_total_hours = 8 + 10 + 7 + 9 + 8  
    expected_pay = (39 * 100.0) + (3 * 150.0)

    assert report["total_hours"] == float(expected_total_hours)
    assert report["total_standard_hours"] == float(expected_standard)
    assert report["total_overtime_hours"] == float(expected_overtime)
    assert report["total_pay"] == float(expected_pay)
