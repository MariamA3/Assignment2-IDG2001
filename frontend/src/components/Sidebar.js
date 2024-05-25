import GetCategories from "./GetCategories";
import LogoutButton from "./LogoutButton";
import "../styles/Sidebar.css";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-content">
        <h2>Categories:</h2>
        {/* Fetch the categories for the sidebar here */}
        <GetCategories />
      </div>
      {/* Add a button for logout */}
      <div className="bottom-container">
        <LogoutButton />
      </div>
    </aside>
  );
}

export default Sidebar;
