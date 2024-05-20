import { useEffect, useState } from "react";
import { useLocation, Link, useParams } from "react-router-dom";
import axiosInstance from "../api/axios";
import { useAuth } from "../context/AuthContext";
import GetPosts from "../components/GetPosts";
import categoryLogo from "../assets/plus-icon.svg";
import "../styles/Categories.css";

// Categories component to display the posts under a specific category
function Categories() {
  const { categoryName } = useParams();
  const [categoryId, setCategoryId] = useState(null);
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  // Format the path to display it as a header will only be shown in mobile view since they dont have the nav header
  const formatPath = (path) => {
    if (path === "/") return "Home";
    return path.charAt(1).toUpperCase() + path.slice(2);
  };

  // Fetch the category ID when the component mounts
  useEffect(() => {
    axiosInstance.get(`/categories/name/${categoryName}`).then((response) => {
      const category = response.data;
      if (category && category.category_id) {
        // Set the category ID to be used in the create post page
        setCategoryId(category.category_id);
      } else {
        throw new Error("Category not found or category ID is undefined");
      }
    });
  }, [categoryName]);

  return (
    <div className="categories-container">
      <h2 className="categories-header">{formatPath(location.pathname)}</h2>
      <div className="categories-link">
        {isAuthenticated ? (
          <Link
            to={{
              // This is to send the category to the create post page using params
              pathname: `/b/${categoryName}/${categoryId}`,
            }}
          >
            <img
              className="categories-icon"
              src={categoryLogo}
              alt="A plus icon for creating a new post"
            />
            Create a post
          </Link>
        ) : (
          <Link to="/login" className="login-button">
            Login to create a post
          </Link>
        )}
      </div>
      <GetPosts />
    </div>
  );
}

export default Categories;
