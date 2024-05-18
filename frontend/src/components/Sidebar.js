import GetCategories from "./GetCategories";
import "../styles/Sidebar.css";

function Sidebar() {
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
        <button className="logout-button">Logout</button>
      </div>
    </aside>
  );
}

export default Sidebar;
