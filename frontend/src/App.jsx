import React, { useState, useEffect } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState('medium');

  const fetchTasks = async () => {
    try {
      const response = await fetch('http://localhost:8000/tasks');
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const addTask = async () => {
    if (!newTask.trim()) return;
    
    try {
      const response = await fetch('http://localhost:8000/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ desc: newTask, priority: newTaskPriority }),
      });
      
      if (response.ok) {
        setNewTask('');
        setNewTaskPriority('medium');
        await fetchTasks();
      }
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  const completeTask = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: 'PUT',
      });
      
      if (response.ok) {
        await fetchTasks();
      }
    } catch (error) {
      console.error('Error completing task:', error);
    }
  };

  const deleteTask = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${id}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        await fetchTasks();
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', padding: '20px' }}>
      <h1>Tasks</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Enter new task..."
          style={{ 
            padding: '10px', 
            marginRight: '10px', 
            borderRadius: '4px', 
            border: '1px solid #ddd',
            width: '200px'
          }}
          onKeyPress={(e) => e.key === 'Enter' && addTask()}
        />
        <select
          value={newTaskPriority}
          onChange={(e) => setNewTaskPriority(e.target.value)}
          style={{
            padding: '10px',
            marginRight: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            backgroundColor: 'white'
          }}
        >
          <option value="high" style={{ color: '#dc3545' }}>🔴 High</option>
          <option value="medium" style={{ color: '#ffc107' }}>🟡 Medium</option>
          <option value="low" style={{ color: '#28a745' }}>🟢 Low</option>
        </select>
        <button 
          onClick={addTask}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Add Task
        </button>
      </div>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {tasks
          .sort((a, b) => {
            const priorityOrder = { high: 0, medium: 1, low: 2 };
            return priorityOrder[a.priority] - priorityOrder[b.priority];
          })
          .map((task) => {
            const priorityColors = {
              high: '#dc3545',
              medium: '#ffc107', 
              low: '#28a745'
            };
            const prioritySymbols = {
              high: '🔴',
              medium: '🟡',
              low: '🟢'
            };
            
            return (
              <li key={task.id} style={{ 
                marginBottom: '10px', 
                padding: '10px', 
                border: '1px solid #eee', 
                borderRadius: '4px',
                borderLeftWidth: '4px',
                borderLeftColor: priorityColors[task.priority],
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ 
                    fontSize: '16px'
                  }}>
                    {prioritySymbols[task.priority]}
                  </span>
                  <span style={{ 
                    textDecoration: task.completed ? 'line-through' : 'none',
                    color: task.completed ? '#666' : '#000'
                  }}>
                    {task.description}
                  </span>
                  <span style={{
                    fontSize: '12px',
                    backgroundColor: priorityColors[task.priority],
                    color: 'white',
                    padding: '2px 6px',
                    borderRadius: '12px',
                    textTransform: 'uppercase',
                    fontWeight: 'bold'
                  }}>
                    {task.priority}
                  </span>
                </div>
            
            <div>
              {!task.completed && (
                <button 
                  onClick={() => completeTask(task.id)}
                  style={{
                    marginRight: '10px',
                    padding: '5px 10px',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Complete
                </button>
              )}
              <button 
                onClick={() => deleteTask(task.id)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#dc3545',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Delete
              </button>
            </div>
          </li>
            );
          })}
      </ul>

      {tasks.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>No tasks yet. Add one above!</p>
      )}
    </div>
  );
}

export default App; 