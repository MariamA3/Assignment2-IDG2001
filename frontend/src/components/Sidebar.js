import { useAuth } from "../context/AuthContext";
import GetCategories from "./GetCategories";
import { useNavigate } from "react-router-dom";
import "../styles/Sidebar.css";

function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Wait for the logout request to complete
      await logout();

      // Redirect to the login page after successful logout
      navigate("/login");
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-content">
        <h2>Categories:</h2>
        {/* Add the fetching for categories here and display them let the user press a category and user will then 
        see all the posts in that category on the home page */}
        <GetCategories />
      </div>
      {/* Add a button to logout (will be added when the login and logout functionality is finished in the backend) */}
      <div className="bottom-container">
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
