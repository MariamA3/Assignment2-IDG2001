import React, { useState, useEffect } from "react";
import Loading from "../components/Loading";
import axiosInstance from "../api/axios";
import "../styles/GetCategories.css";

function GetCategories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch the data on mount and set the categories
  useEffect(() => {
    axiosInstance
      .get("/categories")
      .then((response) => {
        setCategories(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
      });
  }, []);

  // If data is still loading, display a loading screen
  if (loading) {
    return <Loading />;
  }

  return (
    <div className="category-container">
      <ul>
        {categories.map((category, index) => (
          <li key={index}>
            <p>b/{category.name}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GetCategories;
