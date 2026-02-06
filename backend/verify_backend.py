import requests
import datetime
import time
import sys

BASE_URL = "http://localhost:8000"

def log(msg):
    print(f"[TEST] {msg}")

def verify_backend():
    # Wait for server to be up (manual step usually, but here we assume it's running or we can't test)
    # Since I cannot start a background server easily and poll it in one go without blocking, 
    # I will assume the user or a separate process starts it. 
    # However, for this tests to pass, I need the server running.
    # I will attempt to run the test assuming the user acts on it, OR 
    # I will start the server in background now, wait a bit, run tests, then kill it.
    pass

# Refined Plan:
# 1. Start uvicorn in background.
# 2. Run this script.
# 3. Kill uvicorn (optional, or leave it).

if __name__ == "__main__":
    # Test Data
    employee_data = {
        "name": "Test User",
        "email": f"test_{int(time.time())}@example.com",
        "department": "Engineering",
        "role": "Developer",
        "hourly_rate": 100.0,
        "is_active": True
    }

    try:
        # 1. Create Employee
        log("Creating Employee...")
        res = requests.post(f"{BASE_URL}/employees/", json=employee_data)
        if res.status_code != 200:
            log(f"Failed to create employee: {res.text}")
            sys.exit(1)
        employee = res.json()
        emp_id = employee['id']
        log(f"Employee created: ID {emp_id}")

        # 2. Login (Check-in)
        log("Checking in...")
        res = requests.post(f"{BASE_URL}/attendance/login/{emp_id}")
        if res.status_code != 200:
             log(f"Check-in failed: {res.text}")
             sys.exit(1)
        log("Checked in successfully.")

        # Sleep briefly to have difference in time (optional, mocked usually)
        time.sleep(1)

        # 3. Logout (Check-out)
        log("Checking out...")
        res = requests.post(f"{BASE_URL}/attendance/logout/{emp_id}")
        if res.status_code != 200:
             log(f"Check-out failed: {res.text}")
             sys.exit(1)
        data = res.json()
        log(f"Checked out. Total hours: {data['total_hours']}")

        # 4. Payroll Report
        log("Generating Payroll Report...")
        today = datetime.date.today().isoformat()
        report_req = {
            "employee_id": emp_id,
            "start_date": today,
            "end_date": today
        }
        res = requests.post(f"{BASE_URL}/payroll/report", json=report_req)
        if res.status_code != 200:
             log(f"Report failed: {res.text}")
             sys.exit(1)
        report = res.json()
        log(f"Report generated. Total Pay: {report['total_pay']}")

        log("ALL TESTS PASSED")

    except Exception as e:
        log(f"Exception: {e}")
        sys.exit(1)
