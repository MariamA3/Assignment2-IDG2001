import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { toast } from "react-toastify";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import GoBackButton from "./GoBack";
import "../styles/CreatePost.css";

function CreatePost() {
  const categoryId = useParams().categoryId;
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Define state for post
  const [post, setPost] = useState({
    title: "",
    content: "",
    user_id: currentUser.user_id,
    category_id: categoryId,
  });

  // Function to handle adding a new post
  const handleAddPost = async () => {
    setLoading(true);
    try {
      // Send POST request to create a new post
      await axiosInstance.post("/posts", post);
      setLoading(false);

      toast.success("Post created successfully!");

      // Clear the form fields after successful post creation
      setPost({
        title: "",
        content: "",
        user_id: "", 
        category_id: "",
      });

      // Redirect the user to a specific page after successful post creation
      // For example, you can redirect them back to the list of posts
      navigate(-1);
    } catch (error) {
      // Log the error and stop loading even if an error occurs (Or infinite loading will occur)
      console.error("Failed to create post:", error);
      toast.error("Failed to create post. Please try again later.");
      setLoading(false);
    }
  };

  // Function to handle changes in input fields
  const handlepostChange = (event) => {
    const { name, value } = event.target;
    // Update the corresponding field in the post state
    setPost((prevPost) => ({
      ...prevPost,
      [name]: value,
    }));
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="create-post">
      <h2>Create a new post</h2>

      <label className="create-post-content-wrapper">
        <input
          type="text"
          id="title"
          placeholder="Title"
          name="title"
          value={post.title}
          onChange={handlepostChange}
        />
      </label>

      <label className="create-post-content-wrapper">
        <textarea
          id="content"
          placeholder="Write your text here"
          name="content"
          value={post.content}
          onChange={handlepostChange}
        />
      </label>

      <label className="create-post-content-wrapper">
        <button type="submit" onClick={handleAddPost}>
          Create post
        </button>
      </label>

      <GoBackButton>Go Back</GoBackButton>
    </div>
  );
}

export default CreatePost;
