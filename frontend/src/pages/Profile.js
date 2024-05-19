import { useAuth } from "../context/AuthContext";

function Profile() {
  const { currentUser } = useAuth();

  if (!currentUser) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Profile</h1>
      <p>Username: {currentUser.username} </p>
      <p>email: {currentUser.email} </p>
    </div>
  );
}

export default Profile;
