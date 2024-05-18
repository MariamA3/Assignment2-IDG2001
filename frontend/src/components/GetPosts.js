import React, { useState, useEffect } from "react";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import "../styles/GetPosts.css";
import { useParams } from "react-router-dom";

// GetPosts component to fetch posts by category name and display 
// them to the user when they press the categories on the sidebar
function GetPosts() {
  // Get the category name from the URL
  const { categoryName } = useParams();
  const [posts, setPosts] = useState([]);
  const [likes, setLikes] = useState({});
  const [loading, setLoading] = useState(true);

  // Find the category ID by category name and then fetch the posts
  useEffect(() => {
    if (categoryName) {
      // Set loading to true before starting to fetch data
      setLoading(true);
      // Clear the previous set of posts when fetching again
      setPosts([]); 
      // Fetch the category by name
      axiosInstance
        .get(`/categories/name/${encodeURIComponent(categoryName)}`)
        .then((response) => {
          const category = response.data;
          // Fetch the posts by category ID if the category is found
          if (category && category.category_id) {
            return axiosInstance.get(`/posts/category/${category.category_id}`);
          } else {
            throw new Error("Category not found or category ID is undefined");
          }
        })
        // Set the posts to the state and stop loading
        .then((response) => {
          if (response.data) {
            setPosts(
              Array.isArray(response.data) ? response.data : [response.data]
            );
          } else {
            // Set posts to an empty array if no posts are found
            setPosts([]);
          }
          setLoading(false);
        })
        .catch((error) => {
          // Log the error and stop loading even if an error occurs (Or infinite loading will occur)
          console.error("Error fetching data: ", error);
          setLoading(false);
        });
    }
  }, [categoryName]);

  // We need to add some functionality for liking posts
  // Will look at it later
  const handleLike = (postId) => {
    setLikes({ ...likes, [postId]: (likes[postId] || 0) + 1 });
  };

  // Display loading screen while fetching data
  if (loading) {
    return <Loading />;
  }

  // Display a message if no posts are found
  if (posts.length === 0) {
    return <div>No posts found for this category</div>;
  }

  return (
    <div>
      {posts.map((post) => (
        <div key={post.post_id} className="post-container">
          <h2 className="post-title">Title: {post.title}</h2>
          <p className="post-content">Content: {post.content}</p>
          <p className="post-footer">Category: {post.category_id}</p>
          <p className="post-footer">Date: {post.date}</p>
          {/* Add a like button to like the post we dont have that functionality yet */}
          <button
            onClick={() => handleLike(post.post_id)}
            className="like-button"
          >
            <span>Like</span>
            <span>
              {likes[post.post_id] === 1
                ? "1 like"
                : `${likes[post.post_id] || 0} likes`}
            </span>
          </button>
        </div>
      ))}
    </div>
  );
}

export default GetPosts;
