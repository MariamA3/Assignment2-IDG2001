import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../api/axios";
import GoBackButton from "../components/GoBack";
import "../styles/UserProfile.css";

function UserProfile() {
  const { username } = useParams();
  const { currentUser } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    axiosInstance.get(`/${username}`).then((response) => {
      setProfile(response.data);
    });
  }, [username]);

  if (!profile) return <div>Loading...</div>;

  console.log(profile)

  return (
    <div className="profile-container">
      <h2>{profile.username} profile</h2>
      <p>Username: {profile.username}</p>
      <p>Email: {profile.email}</p>
      {currentUser && currentUser.username === profile.username && <button>Delete Account</button>}
      <GoBackButton>Go Back</GoBackButton>
    </div>
  );
}

export default UserProfile;
