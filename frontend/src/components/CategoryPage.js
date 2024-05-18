import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../api/axios";
import Loading from "./Loading";
import GetPosts from "./GetPosts";

const CategoryDetails = () => {
  const { category_id } = useParams();
  const [loading, setLoading] = useState(true);
  const [posts, setPosts] = useState([]);

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

  if (!category_id) {
    return <div>No category selected</div>;
  }

  if (loading) {
    return <Loading />;
  }

  // Check if there are no posts for the selected category
  if (posts.length === 0) {
    return <div>No posts found for this category</div>;
  }

  return (
    <div>
      <h1>{category_id}</h1>
      {/* Render the posts here */}
      {posts.map((post, index) => (
        <GetPosts key={index} post={post} />
      ))}
    </div>
  );
};

export default CategoryDetails;
