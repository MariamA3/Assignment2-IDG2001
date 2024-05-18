/*
import { useLocation, Link, useParams } from "react-router-dom";
import GetPosts from "../components/GetPosts";
import categoryLogo from "../assets/plus-icon.svg";
import "../styles/Categories.css";

function Categories() {
  const { categoryName } = useParams();
  const location = useLocation();

  const formatPath = (path) => {
    if (path === "/") return "Home";
    return path.charAt(1).toUpperCase() + path.slice(2);
  };

  return (
    <div className="categories-container">
      <h2 className="categories-header">{formatPath(location.pathname)}</h2>
      <div className="categories-link">
        <Link
          to={{
            pathname: `/b/${categoryName}/post`,
            state: { categoryId: category_id },
          }}
        >
          <img
            className="categories-icon"
            src={categoryLogo}
            alt="A plus icon for creating a new post"
          />
          Create a post
        </Link>
      </div>
      <GetPosts />
    </div>
  );
}

export default Categories;
*/