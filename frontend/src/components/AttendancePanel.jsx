import React, { useState } from 'react';
import axios from 'axios';

const AttendancePanel = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const [manualDate, setManualDate] = useState('');
  const [stdHours, setStdHours] = useState('');
  const [otHours, setOtHours] = useState('');
  const [csvFile, setCsvFile] = useState(null);

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

  const handleManualAdd = async () => {
    setMessage(null);
    setError(null);
    try {
      await axios.post('http://localhost:8000/attendance/manual', {
        employee_id: employeeId, 
        date: manualDate,
        standard_hours: parseFloat(stdHours),
        overtime_hours: parseFloat(otHours)
      });
      setMessage('Manual entry added successfully');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add manual entry');
    }
  };

  const handleCsvUpload = async () => {
     if (!csvFile) {
        setError("Please select a file first");
        return;
     }
     const formData = new FormData();
     formData.append('file', csvFile);

     try {
        const res = await axios.post('http://localhost:8000/attendance/manual/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        setMessage(`Upload processed. Success: ${res.data.success_count}, Errors: ${res.data.errors.length}`);
        if(res.data.errors.length > 0) {
            console.error(res.data.errors);
            setError("Some rows failed. Check console for details."); 
        }
     } catch (err) {
        setError(err.response?.data?.detail || 'Upload failed');
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
      
      <hr style={{margin: '20px 0'}} />

      {/* Manual Entry */}
      <div className="manual-entry-section">
        <h3>Manual Attendance Entry</h3>
        <div className="form-group" style={{maxWidth: '300px', marginBottom: '10px'}}>
            <label>Date:</label>
            <input type="date" value={manualDate} onChange={(e) => setManualDate(e.target.value)} className="form-control" />
        </div>
        <div className="form-group" style={{maxWidth: '300px', marginBottom: '10px'}}>
            <label>Standard Hours:</label>
            <input type="number" step="0.1" value={stdHours} onChange={(e) => setStdHours(e.target.value)} className="form-control" placeholder="e.g. 8.0" />
        </div>
        <div className="form-group" style={{maxWidth: '300px', marginBottom: '10px'}}>
            <label>Overtime Hours:</label>
            <input type="number" step="0.1" value={otHours} onChange={(e) => setOtHours(e.target.value)} className="form-control" placeholder="e.g. 2.0" />
        </div>
        <button className="btn btn-primary" onClick={handleManualAdd}>Add Manual Entry</button>
      </div>

      <hr style={{margin: '20px 0'}} />

      {/* Bulk Upload */}
      <div className="bulk-upload-section">
        <h3>Bulk Upload (CSV)</h3>
        <p><small>Format: employee_email, date, standard_hours, overtime_hours</small></p>
        <input type="file" accept=".csv" onChange={(e) => setCsvFile(e.target.files[0])} />
        <button className="btn btn-warning" onClick={handleCsvUpload} style={{marginTop: '10px'}}>Upload CSV</button>
      </div>

      {message && <div style={{marginTop: '15px', color: 'green', fontWeight: 'bold'}}>{message}</div>}
      {error && <div style={{marginTop: '15px', color: 'red', fontWeight: 'bold'}}>{error}</div>}
    </div>
  );
};

export default AttendancePanel;
