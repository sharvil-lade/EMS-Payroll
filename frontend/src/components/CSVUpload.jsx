import React, { useState } from 'react';
import axios from 'axios';

const CSVUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setIsUploading(true);
    try {
      await axios.post('http://localhost:8000/employees/upload-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage('Employees uploaded successfully!');
      setFile(null);
      // Reset file input
      document.getElementById('csvMsg').value = ""; 
      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Error uploading file.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: '20px', padding: '20px' }}>
      <h3>Upload Employees via CSV</h3>
      <p style={{fontSize: '0.9rem', color: '#666'}}>
        CSV should have headers: <strong>name, email, department, role, hourly_rate</strong>
      </p>
      <form onSubmit={handleUpload} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleFileChange} 
          id="csvMsg"
        />
        <button 
          type="submit" 
          className="btn btn-secondary" 
          disabled={isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload CSV'}
        </button>
      </form>
      {message && <p style={{ color: 'green', marginTop: '10px' }}>{message}</p>}
      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
};

export default CSVUpload;
