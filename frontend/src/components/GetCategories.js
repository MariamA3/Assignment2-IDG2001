import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";
import Loading from "../components/Loading";
import axiosInstance from "../api/axios";
import "../styles/GetCategories.css";

function GetCategories() {
  const { category_id } = useParams();
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
        console.error("Error fetching data: ", error);
        setLoading(false);
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
            {/* Use category.category_id instead of category_id */}
            <Link to={`/b/${category.category_id}`}>
              <p>b/{category.name}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GetCategories;
