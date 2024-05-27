import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import "../styles/GetPosts.css";
import "../styles/Categories.css";

function GetPosts() {
  const { categoryName } = useParams();
  const [posts, setPosts] = useState([]);
  const [likes, setLikes] = useState({});
  const [loading, setLoading] = useState(true);

  // Fetch the posts for the category when the component mounts or when the category name changes
  useEffect(() => {
    if (categoryName) {
      setLoading(true);

      // First, fetch the category data using the categoryName
      axiosInstance
        .get(`/categories/name/${categoryName}`)
        .then((response) => {
          const category = response.data;
          // If the category data is valid and the category ID is defined, fetch the posts for this category
          if (category && category.category_id) {
            return axiosInstance.get(`/posts/category/${category.category_id}`);
          } else {
            throw new Error("Category not found or category ID is undefined");
          }
        })
        .then((response) => {
          // If the posts data is an array and it contains at least one post,
          // fetch the username for each post, will be used to display username
          const posts = response.data;
          if (Array.isArray(posts) && posts.length > 0) {
            const postPromises = posts.map((post) =>
              axiosInstance
                .get(`/users/${post.user_id}`)
                .then((userResponse) => {
                  // If the user data is fetched successfully, add the username to the post data
                  return { ...post, username: userResponse.data.username };
                })
                .catch((error) => {
                  // If the user data is not fetched successfully, add an error message to the post data
                  if (error.response && error.response.status === 404) {
                    return { ...post, username: "User not found" };
                  } else {
                    return { ...post, username: "Error fetching user" };
                  }
                })
            );
            // Wait for all postPromises to resolve
            return Promise.all(postPromises);
          } else {
            // If no posts are found for this category, throw an error
            throw new Error("No posts found for this category");
          }
        })
        .then((postsWithUsernames) => {
          setPosts(postsWithUsernames);
        })
        .catch((error) => {
          setPosts([]);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [categoryName]);

  // Function to handle liking a post
  const handleLike = async (postId) => {
    try {
      // Get the user ID from the post data
      const userId = posts[0].user_id;
      // Check if the current user has already liked this post
      const response = await axiosInstance.post("/like", {
        user_id: userId,
        post_id: postId,
      });
      if (response.status === 200) {
        setLikes({ ...likes, [postId]: (likes[postId] || 0) + 1 });
        // Update the userLikes state to indicate that the current user has liked this post
      } else {
        console.error(response.data.message);
      }
    } catch (error) {
      console.error("Error liking post:", error.message);
    }
  };

  // Display a loading spinner while fetching data
  if (loading) {
    return <Loading />;
  }

  // Display a message if no posts are found for the category
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
          <h2 className="post-title">{post.title}</h2>
          <p className="post-content">{post.content}</p>
          <p className="post-footer">Posted by: {post.username}</p>
          <p className="post-footer">Date: {post.created_at}</p>
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
