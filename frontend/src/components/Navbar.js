import { Link } from "react-router-dom";
import logo from "../assets/bread.svg";
import "../styles/Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="left-section">
        <img src={logo} alt="A piece of bread" />
        <h1>Breadit</h1>
      </div>
      <div className="right-section">
        {/* User can log in the idea is that the user has to log in to post something for a category */}
        {/* Should probably allow the user to go to a profile page if they're logged in */}
        <p>
          <Link to="/login">Login</Link>
        </p>
      </div>
    </nav>
  );
}

export default Navbar;
