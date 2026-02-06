import urllib.request
import urllib.error
import json
import datetime
import time
import sys

BASE_URL = "http://localhost:8000"

def log(msg):
    print(f"[TEST] {msg}")

def request(method, url, data=None, params=None):
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    if data:
        json_data = json.dumps(data).encode('utf-8')
        req.data = json_data
        
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            try:
                json_response = json.loads(response_body)
            except:
                json_response = response_body
            return status_code, json_response
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)

if __name__ == "__main__":
    # Test Data
    employee_data = {
        "name": "Test MultiSession",
        "email": f"test_multi_{int(time.time())}@example.com",
        "department": "Engineering",
        "role": "QA",
        "hourly_rate": 200.0,
        "is_active": True
    }

    try:
        # 1. Create Employee
        log("Creating Employee...")
        status, employee = request("POST", f"{BASE_URL}/employees/", data=employee_data)
        if status != 200:
            log(f"Failed to create employee: {employee}")
            sys.exit(1)
        emp_id = employee['id']
        log(f"Employee created: ID {emp_id}")

        # 2. Session 1: Login
        log("Session 1: Checking in...")
        status, res = request("POST", f"{BASE_URL}/attendance/login/{emp_id}")
        if status != 200:
             log(f"Check-in 1 failed: {res}")
             sys.exit(1)
        log("Session 1: Checked in.")
        
        time.sleep(1) # Simulate work

        # Session 1: Logout
        log("Session 1: Checking out...")
        status, data = request("POST", f"{BASE_URL}/attendance/logout/{emp_id}")
        if status != 200:
             log(f"Check-out 1 failed: {data}")
             sys.exit(1)
        session1_hours = data['total_hours']
        log(f"Session 1 ended. Duration: {session1_hours} hours")

        # 3. Session 2: Login
        log("Session 2: Checking in...")
        status, res = request("POST", f"{BASE_URL}/attendance/login/{emp_id}")
        if status != 200:
             log(f"Check-in 2 failed: {res}")
             sys.exit(1)
        log("Session 2: Checked in.")

        time.sleep(1) # Simulate work

        # Session 2: Logout
        log("Session 2: Checking out...")
        status, data = request("POST", f"{BASE_URL}/attendance/logout/{emp_id}")
        if status != 200:
             log(f"Check-out 2 failed: {data}")
             sys.exit(1)
        session2_hours = data['total_hours']
        log(f"Session 2 ended. Duration: {session2_hours} hours")

        # 4. Verify Attendance Report
        log("Verifying Attendance Report...")
        today = datetime.date.today().isoformat()
        status, report = request("GET", f"{BASE_URL}/attendance/report", params={
            "employee_id": emp_id,
            "start_date": today,
            "end_date": today
        })
        if status != 200:
             log(f"Attendance Report failed: {report}")
             sys.exit(1)
        
        log(f"Report Data: {report}")
        
        # Check sessions count
        assert report['total_sessions'] == 2, f"Expected 2 sessions, got {report['total_sessions']}"
        assert len(report['daily_breakdown']) == 1, "Expected 1 day in breakdown"
        assert report['daily_breakdown'][0]['sessions_count'] == 2, "Expected 2 sessions in daily breakdown"
        
        expected_total_hours = round(session1_hours + session2_hours, 2)
        # Allow small float diff
        assert abs(report['total_hours'] - expected_total_hours) < 0.01, f"Expected {expected_total_hours}, got {report['total_hours']}"
        
        log("Attendance Report Verified.")

        log("Attendance Report Verified.")

        # 5. Verify Payroll Report
        log("Verifying Payroll Report...")
        report_req = {
            "employee_id": emp_id,
            "start_date": today,
            "end_date": today
        }
        status, pay_report = request("POST", f"{BASE_URL}/payroll/report", data=report_req)
        if status != 200:
             log(f"Payroll Report failed: {pay_report}")
             sys.exit(1)
        
        expected_pay = round(expected_total_hours * 200.0, 2) # hourly rate 200
        
        # Check total pay
        assert abs(pay_report['total_hours'] - expected_total_hours) < 0.01, f"Payroll hours mismatch: {pay_report['total_hours']} != {expected_total_hours}"
        log(f"Payroll Report: Total Pay {pay_report['total_pay']}, Expected ~{expected_pay}")
        
        log("ALL TEST SCENARIOS PASSED")

    except Exception as e:
        log(f"Exception: {e}")
        sys.exit(1)
