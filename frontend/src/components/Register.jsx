import { useState } from "react";
import axios from "axios";
import "/src/components/Register.css"

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    phone_number: ""
  });

  const [errorMessage, setErrorMessage] = useState(""); // Track errors
  const [successMessage, setSuccessMessage] = useState(""); // Track success

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(""); // Clear previous errors
    setSuccessMessage(""); // Clear previous success messages

    try {
      const response = await axios.post("http://localhost:6060/register", formData);
      setSuccessMessage(response.data.message); // Show success message
      setFormData({ username: "", email: "", password: "", phone_number: "" }); // Clear form
    } catch (error) {
      // Show error if registration fails
      const errorResponse = error.response?.data?.error || "An error occurred. Please try again.";
      setErrorMessage(errorResponse);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Register</h2>
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
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={formData.email}
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
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
            <label htmlFor="phone_number" className="form-label">Phone Number</label>
            <p className="form-description">
                Please provide your phone number to receive task reminders via SMS.
            </p>
            <input
                type="text"
                className="form-control"
                id="phone_number"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                required
            />
            </div>
        <button type="submit" className="btn btn-primary">Register</button>
      </form>
    </div>
  );
};

export default Register;

