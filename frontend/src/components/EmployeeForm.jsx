import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

const EmployeeForm = () => {
  const [employee, setEmployee] = useState({
    name: '',
    email: '',
    department: '',
    role: '',
    hourly_rate: 0,
    overtime_rate: 0,
    is_active: true
  });
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;

  useEffect(() => {
    if (isEdit) {
      fetchEmployee();
    }
  }, [id]);

  const fetchEmployee = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/employees/${id}`);
      setEmployee(response.data);
    } catch (error) {
      console.error('Error fetching employee:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEmployee({ ...employee, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await axios.put(`http://localhost:8000/employees/${id}`, employee);
      } else {
        await axios.post('http://localhost:8000/employees/', employee);
      }
      navigate('/employees');
    } catch (error) {
      console.error('Error saving employee:', error);
    }
  };

  return (
    <div className="card" style={{maxWidth: '600px', margin: '0 auto'}}>
      <h2>{isEdit ? 'Edit Employee' : 'Add New Employee'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name</label>
          <input type="text" name="name" value={employee.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" name="email" value={employee.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Department</label>
          <input type="text" name="department" value={employee.department} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Role</label>
          <input type="text" name="role" value={employee.role} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Hourly Pay Rate (₹)</label>
          <input type="number" name="hourly_rate" value={employee.hourly_rate} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Overtime Pay Rate (₹)</label>
          <input type="number" name="overtime_rate" value={employee.overtime_rate} onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-success">{isEdit ? 'Update' : 'Create'}</button>
      </form>
    </div>
  );
};

export default EmployeeForm;
