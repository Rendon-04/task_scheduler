import { useState } from "react";
import axios from "axios";

const Login = ({ setUser }) => {
  // State to track form inputs
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });

  // State to track success or error messages
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({ ...credentials, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(""); // Clear previous errors
    setSuccessMessage(""); // Clear previous success messages

    try {
      const response = await axios.post("http://localhost:6060/login", credentials);
      setSuccessMessage("Login successful!");
      setUser(response.data.user_id); // Set user ID in parent state
    } catch (error) {
      // Handle errors and display appropriate messages
      const errorResponse = error.response?.data?.error || "An error occurred. Please try again.";
      setErrorMessage(errorResponse);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Login</h2>
      {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            id="username"
            name="username"
            value={credentials.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={credentials.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
    </div>
  );
};

export default Login;


