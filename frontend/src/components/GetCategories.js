import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import Loading from "../components/Loading";
import axiosInstance from "../api/axios";
import "../styles/GetCategories.css";

function GetCategories({ closeMenu }) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axiosInstance
      .get("/categories")
      .then((response) => {
        setCategories(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setLoading(false);
        toast.error("Failed to fetch categories. Please try again later.");
        console.error("Error fetching data: ", error);        
      });
  }, []);

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="category-container">
      <ul>
        {categories.map((category, index) => (
          <li key={index}>
            <Link to={`/b/${category.name}`} onClick={closeMenu}>
              <p>b/{category.name}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GetCategories;
