import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles/Auth.css";


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  /*
  const [isLoading, setIsLoading] = useState(false); 
  */
  const navigate = useNavigate(); 

  const handleChange = (event) => {
    const { name, value } = event.target;
    if (name === "email") setEmail(value);
    if (name === "password") setPassword(value);
  };

  /*
  const validateInputs = () => {
    if (!email || !password) {
      return false;
    }
    if (!email.includes("@")) {
      return false;
    }
    return true;
  };
  */

  /*
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateInputs()) return; 

    setIsLoading(true); 
    try {
      await auth.login({ email, password }); 
      toast.success("Logged in successfully.");
      navigate("/dashboard"); 
    } catch (error) {
      toast.error(
        "Login failed. Please check if your email or password is correct."
      );
    } finally {
      setIsLoading(false); 
    }
  };
  */

  return (
    <div className="register-login-wrapper">
      <div className="back-to-home-container">
        <button onClick={() => navigate("/")} className="back-to-home-btn">
          ⬅ Back
        </button>
      </div>
      <div className="register-login-content">
        <h2>Login</h2>
        <form noValidate>
          <div>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              name="email"
              value={email}
              onChange={handleChange}
              placeholder="Enter your email"
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

          <button type="submit"></button>
        </form>
        <p>
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
