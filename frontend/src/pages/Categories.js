import GetPosts from "../components/GetPosts";
import { useLocation } from "react-router-dom";
import "../styles/Categories.css";

function Categories() {
  const location = useLocation();

  const formatPath = (path) => {
    if (path === "/") return "Home";
    return path.charAt(1).toUpperCase() + path.slice(2);
  };

  return (
    <div className="categories-container">
      <h2 className="categories-header">{formatPath(location.pathname)}</h2>
      <GetPosts />
    </div>
  );
}

export default Categories;
