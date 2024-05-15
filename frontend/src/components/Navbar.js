import { Link } from 'react-router-dom';
import "../styles/Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <h1>Navbar</h1>
            {/* User can log in the idea is that the user has to log in to post something for a category */}
            {/* Should probably allow the user to go to a profile page if they're logged in */}
            <p><Link to="/login">Login</Link></p>
        </nav>
    );
}

export default Navbar;