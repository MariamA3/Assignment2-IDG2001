import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import userIcon from "../assets/user.svg";
import logo from "../assets/bread.svg";
import "../styles/Navbar.css";

function Navbar() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  // Function to format the path
  // Will be used to display the current location of the user in the navbar
  const formatPath = (path) => {
    if (path === "/") return "Home";
    return path.charAt(1).toUpperCase() + path.slice(2);
  };

  return (
    <nav className="navbar">
      <div className="left-section">
        <img src={logo} alt="A piece of bread" />
        <h1>Breadit</h1>
      </div>

      <h2>{formatPath(location.pathname)}</h2>
      <div className="right-section">
        {/* User can log in the idea is that the user has to log in to post something for a category */}
        {/* Should probably allow the user to go to a profile page if they're logged in */}
        {isAuthenticated ? (
          <Link to="/profile">
            <img src={userIcon} alt="User icon" />
          </Link>
        ) : (
          <Link to="/login" className="login-button">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
