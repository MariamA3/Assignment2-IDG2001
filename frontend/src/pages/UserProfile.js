import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../api/axios";
import GoBackButton from "../components/GoBack";
import "../styles/UserProfile.css";

// For the fetching of profiles if the user is logged in allow them to delete the account
function UserProfile() {
  const { username } = useParams();
  const { currentUser, getCookie } = useAuth();
  const [profile, setProfile] = useState(null);
  const [userNotFound, setUserNotFound] = useState(false);

  // Fetch the profile data when the component mounts or when the username changes
  useEffect(() => {
    axiosInstance
      .get(`/${username}`)
      .then((response) => {
        setProfile(response.data);
        setUserNotFound(false);
      })
      .catch((error) => {
        if (error.response && error.response.status === 404) {
          setUserNotFound(true);
        } else {
          console.error("Error fetching data: ", error);
        }
      });
  }, [username]);

  // Display a message if the user is not found
  if (userNotFound) return <div>User not found</div>;

  // Display a loading message while fetching data
  if (!profile) {
    return <div>Loading...</div>;
  }

  // Function to handle deleting the account
  const handleDeleteAccount = async () => {
    if (!profile) {
      console.error("Profile is null");
      return;
    }

    try {
      // Send a DELETE request to delete the user's account we need the csrf token
      await axiosInstance.delete(`/users/${profile.username}`, {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token"),
        },
        withCredentials: true,
      });
      alert("Account deleted successfully");
    } catch (error) {
      console.error("Failed to delete account:", error);
    }
  };

  return (
    <div className="profile-container">
      <h2>{profile.username} profile</h2>
      <p>Username: {profile.username}</p>
      <p>Email: {profile.email}</p>
      {currentUser && currentUser.username === profile.username && (
        <button className="delete-button" onClick={handleDeleteAccount}>Delete Account</button>
      )}
      <GoBackButton>Go Back</GoBackButton>
    </div>
  );
}

export default UserProfile;
