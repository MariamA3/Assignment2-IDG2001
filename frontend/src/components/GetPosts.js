import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import "../styles/GetPosts.css";
import "../styles/Categories.css";

function GetPosts() {
  const { categoryName } = useParams();
  const [posts, setPosts] = useState([]);
  const [likes, setLikes] = useState({});
  const [loading, setLoading] = useState(true);
  const [offset, setOffset] = useState(0); // Track the offset for fetching additional posts

  useEffect(() => {
    if (categoryName) {
      setLoading(true);

      // Fetch the 10 most recent posts initially
      axiosInstance
        .get(`/categories/name/${categoryName}`)
        .then((response) => {
          const category = response.data;
          if (category && category.category_id) {
            return axiosInstance.get(`/posts/category/${category.category_id}?limit=10&offset=${offset}`);
          } else {
            throw new Error("Category not found or category ID is undefined");
          }
        })
        .then((response) => {
          const newPosts = response.data;
          if (Array.isArray(newPosts) && newPosts.length > 0) {
            setPosts((prevPosts) => [...prevPosts, ...newPosts]); // Append new posts to the existing ones
          } else {
            throw new Error("No posts found for this category");
          }
        })
        .catch((error) => {
          console.error("Error fetching posts:", error);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [categoryName, offset]); // Include offset in the dependency array

  // Function to fetch 10 more posts
  const fetchMorePosts = () => {
    setOffset((prevOffset) => prevOffset + 10); // Increment offset by 10
  };

  const handleLike = async (postId) => {
    try {
      const userId = 1; // Replace with the actual user ID
      const response = await axiosInstance.post('/like', { user_id: userId, post_id: postId });
      if (response.status === 200) {
        setLikes({ ...likes, [postId]: (likes[postId] || 0) + 1 });
      } else {
        console.error(response.data.message);
      }
    } catch (error) {
      console.error('Error liking post:', error.message);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (posts.length === 0) {
    return (
      <div>
        <div>No posts found under the category "{categoryName}"</div>
      </div>
    );
  }

  return (
    <div>
      {posts.map((post) => (
        <div key={post.post_id} className="post-container">
          <h2 className="post-title">Title: {post.title}</h2>
          <p className="post-content">Content: {post.content}</p>
          <p className="post-footer">Category: {post.category_id}</p>
          <p className="post-footer">Date: {post.created_at}</p>
          <p className="post-footer">Posted by: {post.username}</p>
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
      <button onClick={fetchMorePosts}>Load More</button> {/* Button to fetch 10 more posts */}
    </div>
  );
}

export default GetPosts;
