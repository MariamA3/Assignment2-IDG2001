import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/Auth.css";

// I have comment out some functionality will be implemented when we have a working backends
function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false); 
  const auth = useAuth();
  const navigate = useNavigate(); 

  const handleChange = (event) => {
    const { name, value } = event.target;
    if (name === "username") setUsername(value);
    if (name === "password") setPassword(value);
  };

  const validateInputs = () => {
    if (!username || !password) {
      return false;
    }
    
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateInputs()) return; 

    setIsLoading(true); 
    try {
      await auth.login({ username, password }); 
      navigate("/profile"); 
    } catch (error) {
      console.error("Failed to login: ", error);
    } finally {
      setIsLoading(false); 
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
        <h2>Login</h2>
        <form onSubmit={handleSubmit} noValidate>
          <div>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="username"
              name="username"
              value={username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
            />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              name="password"
              value={password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" disabled={isLoading}>
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>
        <p>
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
