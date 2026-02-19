import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Users component: Fetching from API endpoint:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users component: Fetched data:', data);
        
        // Support both paginated (.results) and plain array responses
        const usersData = data.results || data;
        console.log('Users component: Processed users:', usersData);
        
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users component: Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return (
    <div className="container mt-4">
      <div className="text-center p-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading users...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>{error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">👤 Users</h2>
        <span className="badge bg-primary">{users.length} Users</span>
      </div>
      
      <div className="table-responsive">
        <table className="table table-hover table-striped align-middle">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Team</th>
              <th scope="col">Fitness Level</th>
              <th scope="col">Date Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map(user => (
                <tr key={user.id}>
                  <td><strong>{user.username || 'N/A'}</strong></td>
                  <td>{user.email || 'N/A'}</td>
                  <td>
                    {user.team_name || user.team ? (
                      <span className="badge bg-secondary">{user.team_name || user.team}</span>
                    ) : (
                      <span className="text-muted">No team</span>
                    )}
                  </td>
                  <td>
                    <span className={`badge ${user.fitness_level === 'Advanced' ? 'bg-success' : user.fitness_level === 'Intermediate' ? 'bg-warning' : 'bg-info'}`}>
                      {user.fitness_level || 'N/A'}
                    </span>
                  </td>
                  <td>{new Date(user.date_joined).toLocaleDateString() || 'N/A'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-muted py-4">No users found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;
