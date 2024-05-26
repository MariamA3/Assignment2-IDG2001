import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../styles/LogoutButton.css";

function LogoutButton() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  // Function to handle logout
  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Logout
    </button>
  );
}

export default LogoutButton;
