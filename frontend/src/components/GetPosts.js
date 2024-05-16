import React, { useState } from "react";
import "../styles/GetPosts.css";

function GetPosts() {
  const [likes, setLikes] = useState(0);

  /* Just for styling and testing the frontend */
  const handleLike = () => {
    setLikes(likes + 1);
  };

  /* Posts should be dynamically fetched from the database and filtered by category  */
  return (
    <>
      <div className="post-container">
        <h1 className="post-title">Title: why dogs are the best</h1>
        <p className="post-content">
          Content: dogs are the best because they are always happy
        </p>
        <p className="post-footer">Category: dogs</p>
        <p className="post-footer">Date: 15/05/2024</p>
        {/* We need to add logic for handling likes */}
        <button onClick={handleLike} className="like-button">
          <span>Like</span>
          <span>{likes === 1 ? "1 like" : `${likes} likes`}</span>{" "}
        </button>
      </div>

      <div className="post-container">
        <h1 className="post-title">Title: why cats are the best</h1>
        <p className="post-content">
          Content: cats are the best because they are always calm
        </p>
        <p className="post-footer">Category: cats</p>
        <p className="post-footer">Date: 16/05/2024</p>
        {/* We need to add logic for handling likes */}
        <button onClick={handleLike} className="like-button">
          <span>Like</span>
          <span>{likes === 1 ? "1 like" : `${likes} likes`}</span>
        </button>
      </div>
    </>
  );
}

export default GetPosts;
