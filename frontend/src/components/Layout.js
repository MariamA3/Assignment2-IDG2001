import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/Layout.css";

const Layout = () => {
  return (
    <div className="layout-container">
      <Navbar />

      <div className="content-container">
        <div className="layout-sidebar"><Sidebar /></div>

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
