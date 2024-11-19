import { useState, useEffect } from "react";
import axios from "axios";

export default function Dashboard({ userId }) {
  // State for tasks and new task creation
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({
    title: "",
    due_date: "",
    description: "",
    priority: "Medium",
  });

  // Fetch tasks from the backend
  const fetchTasks = async () => {
    try {
      const response = await axios.get(`http://localhost:6060/task/${userId}`);
      setTasks(response.data);
    } catch (error) {
      alert("Failed to load tasks!");
    }
  };

  // Handle input changes for creating a new task
  const handleTaskChange = (e) => {
    const { name, value } = e.target;
    setNewTask({ ...newTask, [name]: value });
  };

  // Add a new task
  const addTask = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:6060/tasks", { user_id: userId, ...newTask });
      fetchTasks(); // Refresh tasks after adding
      alert("Task added successfully!");
      setNewTask({ title: "", due_date: "", description: "", priority: "Medium" }); // Reset form
    } catch (error) {
      alert("Failed to add task!");
    }
  };

  // Update an existing task
  const updateTask = async (taskId, updates) => {
    try {
      await axios.put(`http://localhost:6060/tasks/${taskId}`, updates);
      fetchTasks(); // Refresh tasks after updating
      alert("Task updated successfully!");
    } catch (error) {
      alert("Failed to update task!");
    }
  };

  // Delete a task
  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`http://localhost:6060/tasks/${taskId}`);
      fetchTasks(); // Refresh tasks after deleting
      alert("Task deleted successfully!");
    } catch (error) {
      alert("Failed to delete task!");
    }
  };

  // Notify about a specific task
  const notifyTask = async (taskId) => {
    try {
      const response = await axios.post(`http://localhost:6060/notify/${taskId}`);
      alert(response.data.message);
    } catch (error) {
      alert("Failed to send notification!");
    }
  };

  // Fetch tasks when the component is mounted
  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="container">
      <h1>Your Tasks</h1>
      <form onSubmit={addTask} className="mb-4">
        <div className="mb-3">
          <input
            className="form-control"
            name="title"
            placeholder="Task Title"
            value={newTask.title}
            onChange={handleTaskChange}
            required
          />
        </div>
        <div className="mb-3">
          <input
            className="form-control"
            name="due_date"
            type="date"
            value={newTask.due_date}
            onChange={handleTaskChange}
            required
          />
        </div>
        <div className="mb-3">
          <textarea
            className="form-control"
            name="description"
            placeholder="Task Description"
            value={newTask.description}
            onChange={handleTaskChange}
          ></textarea>
        </div>
        <div className="mb-3">
          <select
            className="form-select"
            name="priority"
            value={newTask.priority}
            onChange={handleTaskChange}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">
          Add Task
        </button>
      </form>

      <ul className="list-group">
        {tasks.map((task) => (
          <li key={task.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{task.title}</strong> - {task.due_date}
              <p>{task.description}</p>
              <span className={`badge bg-${task.priority === "High" ? "danger" : task.priority === "Medium" ? "warning" : "success"}`}>
                {task.priority}
              </span>
            </div>
            <div>
              <button
                className="btn btn-success btn-sm me-2"
                onClick={() => updateTask(task.id, { status: "Completed" })}
              >
                Mark as Completed
              </button>
              <button
                className="btn btn-warning btn-sm me-2"
                onClick={() => notifyTask(task.id)}
              >
                Notify
              </button>
              <button
                className="btn btn-danger btn-sm"
                onClick={() => deleteTask(task.id)}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

