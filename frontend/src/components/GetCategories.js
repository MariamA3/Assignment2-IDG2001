import React, { useState, useEffect } from "react";
import "../styles/GetCategories.css";

function GetCategories() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch("http://localhost:4000/categories")
      .then((response) => response.json())
      .then((data) => setCategories(data));
  }, []);

  return (
    <div className="category-container">
       <ul>
        {categories.map((category, index) => (
          <li key={index}>
            b/{category.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GetCategories;
