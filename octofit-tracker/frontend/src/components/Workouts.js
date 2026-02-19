import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts component: Fetching from API endpoint:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts component: Fetched data:', data);
        
        // Support both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts component: Processed workouts:', workoutsData);
        
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts component: Error fetching workouts:', error);
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
        <p className="mt-3">Loading workouts...</p>
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

  const getDifficultyBadge = (level) => {
    const badges = {
      'Beginner': 'bg-success',
      'Intermediate': 'bg-warning',
      'Advanced': 'bg-danger'
    };
    return badges[level] || 'bg-secondary';
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">💪 Workout Suggestions</h2>
        <span className="badge bg-primary">{workouts.length} Workouts</span>
      </div>
      
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map(workout => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body d-flex flex-column">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <h5 className="card-title mb-0">🏋️ {workout.name || 'N/A'}</h5>
                    <span className={`badge ${getDifficultyBadge(workout.difficulty_level)}`}>
                      {workout.difficulty_level || 'N/A'}
                    </span>
                  </div>
                  
                  <p className="card-text flex-grow-1">
                    {workout.description || 'No description available'}
                  </p>
                  
                  <hr />
                  
                  <div className="mb-2">
                    <span className="badge bg-info me-2">{workout.workout_type || 'N/A'}</span>
                  </div>
                  
                  <div className="d-flex justify-content-between align-items-center mt-2">
                    <small className="text-muted">
                      ⏱️ <strong>{workout.duration || 0}</strong> min
                    </small>
                    <small className="text-muted">
                      🔥 <strong>{workout.calories_burned || 0}</strong> cal
                    </small>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No workouts found
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Workouts;
