import React, { useState, useEffect } from "react";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import "../styles/GetPosts.css";
import { useParams } from "react-router-dom";

function GetPosts() {
  const { category_id } = useParams();
  const [posts, setPosts] = useState([]);
  const [likes, setLikes] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (category_id) {
      setLoading(true);
      axiosInstance
        .get(`/posts`)
        .then((response) => {
          // Filter posts based on categoryId
          const filteredPosts = response.data.filter(
            (post) => post.category_id === parseInt(category_id)
          );
          setPosts(filteredPosts);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching data: ", error);
          setLoading(false);
        });
    }
  }, [category_id]);

  const handleLike = (postId) => {
    setLikes({ ...likes, [postId]: (likes[postId] || 0) + 1 });
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <div>
      {posts.map((post) => (
        <div key={post.post_id} className="post-container">
          <h2 className="post-title">Title: {post.title}</h2>
          <p className="post-content">Content: {post.content}</p>
          <p className="post-footer">Category: {post.category_id}</p>
          <p className="post-footer">Date: {post.date}</p>
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
