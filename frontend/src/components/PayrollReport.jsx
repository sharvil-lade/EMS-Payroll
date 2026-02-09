import React, { useState } from 'react';
import axios from 'axios';

const PayrollReport = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const generateReport = async (e) => {
    e.preventDefault();
    setError(null);
    setReport(null);
    try {
      const response = await axios.post('http://localhost:8000/payroll/report', {
        employee_id: employeeId || null,
        start_date: startDate,
        end_date: endDate
      });
      setReport(response.data);
    } catch (err) {
      setError('Error generating report. Check Employee ID and dates.');
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Payroll Report</h2>
      <div className="card">
        <form onSubmit={generateReport} style={{display: 'flex', gap: '15px', alignItems: 'flex-end', flexWrap: 'wrap'}}>
          <div className="form-group" style={{marginBottom: 0}}>
            <label>Employee ID</label>
            <input 
              type="number" 
              value={employeeId} 
              onChange={(e) => setEmployeeId(e.target.value)} 
              required
            />
          </div>
          <div className="form-group" style={{marginBottom: 0}}>
            <label>Start Date</label>
            <input 
              type="date" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)} 
              required 
            />
          </div>
          <div className="form-group" style={{marginBottom: 0}}>
            <label>End Date</label>
            <input 
              type="date" 
              value={endDate} 
              onChange={(e) => setEndDate(e.target.value)} 
              required 
            />
          </div>
          <button type="submit" className="btn btn-primary">Generate Report</button>
        </form>
      </div>

      {error && <p style={{color: 'red'}}>{error}</p>}

      {report && (
        <div className="card" style={{marginTop: '20px'}}>
          <h3>Salary Slip</h3>
          <p><strong>Employee:</strong> {report.employee_name} (ID: {report.employee_id})</p>
          <p><strong>Period:</strong> {report.start_date} to {report.end_date}</p>
          <hr />
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
            <p><strong>Standard Hours:</strong> {report.total_standard_hours} hrs</p>
            <p><strong>Extra Hours:</strong> {report.total_extra_hours} hrs</p>
          </div>
          <p><strong>Total Hours Worked:</strong> {report.total_hours} hrs</p>
          <p><strong>Hourly Rate:</strong> ₹{report.hourly_rate}</p>
          <h3 style={{color: '#27ae60', marginTop: '10px', borderTop: '1px solid #eee', paddingTop: '10px'}}>
            Total Pay: ₹{report.total_pay}
          </h3>
        </div>
      )}
    </div>
  );
};

export default PayrollReport;
