import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

const ActivityReport = () => {
  const { id } = useParams();
  const [employee, setEmployee] = useState(null);
  const [activityData, setActivityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Default to current month
  const today = new Date();
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
  
  const [startDate, setStartDate] = useState(firstDay.toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(today.toISOString().split('T')[0]);

  useEffect(() => {
    fetchEmployee();
  }, [id]);

  useEffect(() => {
    if (id) {
      fetchActivity();
    }
  }, [id, startDate, endDate]);

  const fetchEmployee = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/employees/${id}`);
      setEmployee(response.data);
    } catch (err) {
      console.error("Error fetching employee:", err);
    }
  };

  const fetchActivity = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('http://localhost:8000/attendance/report', {
        params: {
          employee_id: id,
          start_date: startDate,
          end_date: endDate
        }
      });
      setActivityData(response.data);
    } catch (err) {
      console.error("Error fetching activity:", err);
      setError('Failed to fetch activity data.');
      setActivityData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="header-actions">
        <h2>Activity Report: {employee ? employee.name : `Employee #${id}`}</h2>
        <Link to="/employees" className="btn btn-secondary">Back to Employees</Link>
      </div>

      <div className="card">
        <div className="filters" style={{ marginBottom: '20px', display: 'flex', gap: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
          <div className="form-group" style={{marginBottom: 0}}>
            <label>From:</label>
            <input 
              type="date" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="form-group" style={{marginBottom: 0}}>
            <label>To:</label>
            <input 
              type="date" 
              value={endDate} 
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
          <button onClick={fetchActivity} className="btn btn-primary" style={{marginTop: '24px'}}>Filter</button>
        </div>

        {loading && <p>Loading activity data...</p>}
        {error && <p className="error-text" style={{ color: 'var(--danger)' }}>{error}</p>}

        {activityData && (
          <div>
            <div className="dashboard-grid" style={{ marginBottom: '30px', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
              <div className="dashboard-card" style={{padding: '1.5rem'}}>
                <h3>Total Hours</h3>
                <p style={{fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)'}}>{activityData.total_hours}</p>
              </div>
              <div className="dashboard-card" style={{padding: '1.5rem'}}>
                <h3>Total Sessions</h3>
                <p style={{fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)'}}>{activityData.total_sessions}</p>
              </div>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Sessions Count</th>
                  <th>Worked Hours</th>
                </tr>
              </thead>
              <tbody>
                {activityData.daily_breakdown.length === 0 ? (
                  <tr>
                    <td colSpan="3" style={{ textAlign: 'center', padding: '2rem', color: 'var(--secondary)' }}>
                      No activity found for this period.
                    </td>
                  </tr>
                ) : (
                  activityData.daily_breakdown.map((day, index) => (
                    <tr key={index}>
                      <td>{day.date}</td>
                      <td>{day.sessions_count}</td>
                      <td>{day.total_hours}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ActivityReport;
