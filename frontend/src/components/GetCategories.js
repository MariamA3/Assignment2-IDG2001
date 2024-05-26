import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import Loading from "../components/Loading";
import axiosInstance from "../api/axios";
import "../styles/GetCategories.css";

// GetCategories component to fetch categories and display them to the user
function GetCategories({closeMenu}) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch the categories when the component mounts
  useEffect(() => {
    // Set loading to true before starting to fetch data
    axiosInstance
      .get("/categories")
      .then((response) => {
        setCategories(response.data);
        setLoading(false);
      })
      .catch((error) => {
        // Log the error and stop loading even if an error occurs
        setLoading(false);
        toast.error("Failed to fetch categories. Please try again later.");
        console.error("Error fetching data: ", error);        
      });
  }, []);

  // Display a loading spinner while fetching data
  if (loading) {
    return <Loading />;
  }

// Display the categories if they are fetched successfully
return (
  <div className="category-container">
    <ul>
      {/* Check if categories is an array before mapping */}
      {Array.isArray(categories) && categories.map((category, index) => (
        <li key={index}>
          {/* Use category.category_id instead of category_id */}
          <Link to={`/b/${category.name}`} onClick={closeMenu}>
            <p>b/{category.name}</p>
          </Link>
        </li>
      ))}
    </ul>
  </div>
);


export default GetCategories;
