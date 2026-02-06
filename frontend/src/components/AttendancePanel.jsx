import React, { useState } from 'react';
import axios from 'axios';

const AttendancePanel = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    setMessage(null);
    setError(null);
    try {
      const response = await axios.post(`http://localhost:8000/attendance/login/${employeeId}`);
      setMessage(`Login successful for Employee ID: ${response.data.employee_id} at ${new Date(response.data.login_time).toLocaleString()}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  const handleLogout = async () => {
    setMessage(null);
    setError(null);
    try {
      const response = await axios.post(`http://localhost:8000/attendance/logout/${employeeId}`);
      setMessage(`Logout successful. Worked: ${response.data.total_hours} hours.`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Logout failed');
    }
  };

  return (
    <div className="card">
      <h2>Attendance Check-In/Out</h2>
      <div className="form-group" style={{maxWidth: '300px'}}>
        <label>Enter Employee ID:</label>
        <input 
          type="number" 
          value={employeeId} 
          onChange={(e) => setEmployeeId(e.target.value)} 
          placeholder="e.g. 1"
        />
      </div>
      <div style={{marginTop: '10px'}}>
        <button className="btn btn-success" onClick={handleLogin} style={{marginRight: '10px'}}>Login</button>
        <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
      </div>
      {message && <div style={{marginTop: '15px', color: 'green', fontWeight: 'bold'}}>{message}</div>}
      {error && <div style={{marginTop: '15px', color: 'red', fontWeight: 'bold'}}>{error}</div>}
    </div>
  );
};

export default AttendancePanel;
