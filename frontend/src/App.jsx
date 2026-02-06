import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import EmployeeList from './components/EmployeeList';
import EmployeeForm from './components/EmployeeForm';
import AttendancePanel from './components/AttendancePanel';
import ActivityReport from './components/ActivityReport';
import PayrollReport from './components/PayrollReport';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<EmployeeList />} />
            <Route path="/employees/add" element={<EmployeeForm />} />
            <Route path="/employees/edit/:id" element={<EmployeeForm />} />
            <Route path="/attendance" element={<AttendancePanel />} />
            <Route path="/attendance/report/:id" element={<ActivityReport />} />
            <Route path="/payroll" element={<PayrollReport />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

const Dashboard = () => (
  <div style={{textAlign: 'center', marginTop: '30px'}}>
    <h2>Employee Management System</h2>
    <p style={{marginBottom: '40px', color: '#666'}}>Manage your workforce efficiently.</p>
    
    <div className="dashboard-grid">
      <Link to="/employees" className="dashboard-card">
        <h3>Employees</h3>
        <p>Manage employee records, add new hires, and update details.</p>
        <div className="card-action">Go to Employees &rarr;</div>
      </Link>

      <Link to="/attendance" className="dashboard-card">
        <h3>Attendance</h3>
        <p>Track daily check-ins and check-outs for all employees.</p>
        <div className="card-action">Track Attendance &rarr;</div>
      </Link>

      <Link to="/payroll" className="dashboard-card">
        <h3>Payroll</h3>
        <p>Generate salary reports based on working hours and hourly rates.</p>
        <div className="card-action">View Payroll &rarr;</div>
      </Link>
    </div>
  </div>
);

export default App;
