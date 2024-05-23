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

  useEffect(() => {
    if (categoryName) {
      setLoading(true);

      axiosInstance
        .get(`/categories/name/${categoryName}`)
        .then((response) => {
          const category = response.data;
          console.log("Fetched category:", category); // Debug log
          if (category && category.category_id) {
            return axiosInstance.get(`/posts/category/${category.category_id}`);
          } else {
            throw new Error("Category not found or category ID is undefined");
          }
        })
        .then((response) => {
          const posts = response.data;
          console.log("Fetched posts:", posts); // Debug log
          if (Array.isArray(posts) && posts.length > 0) {
            const postPromises = posts.map((post) =>
              axiosInstance
                .get(`/users/${post.user_id}`)
                .then((userResponse) => {
                  return { ...post, username: userResponse.data.username };
                })
                .catch((error) => {
                  if (error.response && error.response.status === 404) {
                    console.error(`User with ID ${post.user_id} not found`);
                    return { ...post, username: "User not found" };
                  } else {
                    console.error("Error fetching user data:", error.message);
                    return { ...post, username: "Error fetching user" };
                  }
                })
            );
            return Promise.all(postPromises);
          } else {
            throw new Error("No posts found for this category");
          }
        })
        .then((postsWithUsernames) => {
          console.log("Posts with usernames:", postsWithUsernames);
          setPosts(postsWithUsernames);
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            console.error("Category not found");
          } else {
            console.error("Error fetching data:", error.message);
          }
          // Clear posts if an error occurs
          setPosts([]); 
        })
        .finally(() => {
          // Ensure loading is set to false even if an error occurs
          setLoading(false); 
        });
    }
  }, [categoryName]);

  const handleLike = (postId) => {
    setLikes({ ...likes, [postId]: (likes[postId] || 0) + 1 });
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
          <p className="post-footer">Date: {post.date}</p>
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
    </div>
  );
}

export default GetPosts;
