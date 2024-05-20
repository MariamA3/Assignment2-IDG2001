import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosInstance from "../api/axios";
import "../styles/Auth.css";

// For registering a new user
function Register() {
  // State to hold form data for all fields
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const validateForm = () => {
    // Required fields check
    if (!formData.username || !formData.email || !formData.password) {
      return false;
    }

    // Email format check using a simple regex pattern for demonstration purposes
    const emailPattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    if (!emailPattern.test(formData.email)) {
      return false;
    }

    // Password length check
    if (formData.password.length < 8) {
      return false;
    }

    // Password must contain at least one uppercase letter and one special character
    const passwordPattern = /^(?=.*[A-Z])(?=.*[!@#$&*]).*$/;
    if (!passwordPattern.test(formData.password)) {
      return false;
    }
    // If all checks pass
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      const response = await axiosInstance.post("/register", formData);
      console.log("Registration successful:", response.data);
      navigate("/login");
    } catch (error) {
      console.error("Registration failed:", error);
    } finally {
      setIsSubmitting(false); // Reset submission status
    }
  };

  return (
    <div className="register-login-wrapper">
      <div className="back-to-home-container">
        <button onClick={() => navigate("/")} className="back-to-home-btn">
          ⬅ Back
        </button>
      </div>
      <div className="register-login-content">
        <h2>Register</h2>
        <form onSubmit={handleSubmit} noValidate>
          <div>
            <label htmlFor="username">Username*</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your full name"
              required
            />
          </div>
          <div>
            <label htmlFor="email">Email*</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email address"
              required
            />
          </div>
          <div>
            <label htmlFor="password">Password*</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Registering..." : "Register"}
          </button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
