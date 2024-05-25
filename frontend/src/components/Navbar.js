import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FaBars, FaTimes } from "react-icons/fa";
import userIcon from "../assets/user.svg";
import logo from "../assets/bread.svg";
import GetCategories from "./GetCategories";
import "../styles/Navbar.css";

// For ;
function Navbar() {
  const { isAuthenticated, currentUser } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  const location = useLocation();

  // Function to format the path
  // Will be used to display the current location of the user in the navbar
  const formatPath = (path) => {
    if (path === "/") return "Home";
    return path.charAt(1).toUpperCase() + path.slice(2);
  };

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  return (
    <nav className="navbar">
      <Link to="/">
        <div className="left-section">
          <img src={logo} alt="A piece of bread" />
          <h1>Breadit</h1>
        </div>
      </Link>

      <h2>{formatPath(location.pathname)}</h2>
      <div className="right-section">
        {!isAuthenticated ? (
          <Link
            to="/login"
            className="login-button"
            style={{ backgroundColor: "orange" }}
          >
            Login
          </Link>
        ) : (
          <Link to={currentUser ? `/u/${currentUser.username}` : "/login"}>
            <img src={userIcon} alt="User icon" />
          </Link>
        )}
        <button onClick={toggleMenu} className="menu-icon">
          {showMenu ? <FaTimes size={30} /> : <FaBars size={30} />}
        </button>
        <div
          className={`menu ${showMenu ? "show" : ""}`}
          style={{ backgroundColor: "white" }}
        >
          <GetCategories closeMenu={toggleMenu} />
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
