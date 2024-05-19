import { useAuth } from "../context/AuthContext";
import GoBackButton from "../components/GoBack";
import "../styles/Profile.css";

function Profile() {
  const { currentUser } = useAuth();

  if (!currentUser) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-container">
      <h2>Profile</h2>
      <p>Username: {currentUser.username} </p>
      <p>email: {currentUser.email} </p>
      <button>Delete user</button>
      <GoBackButton>Go Back</GoBackButton>
    </div>
  );
}

export default Profile;
