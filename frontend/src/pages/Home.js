import "../styles/Home.css";

function Home() {
  return (
    <div className="home-container">
      <h2>Home</h2>
      <h3>Welcome to Breadit!</h3>
      <p>Select one of the categories on the sidebar to get started.</p>
      <p>
        If you want to post your own content, go into one of the categories and
        start posting!
      </p>
      <h3>How to search for a user</h3>
      <p>To search for a user profile, you can use /u/:username.</p>
      <h3>How to view your profile</h3>
      <p>To see your own profile:</p>
      <ul>
        <li>Press the login button on the top right.</li>
        <li>
          After successfully logging in, press the user icon in the top right.
        </li>
      </ul>
      <h3>How to create a post</h3>
      <p>To create a post:</p>
      <ul>
        <li>Log in from the top right by pressing the login button.</li>
        <li>
          Choose a category you want to make a post in from the left sidebar.
        </li>
        <li>
          After choosing a category, press the "Create a New Post" button in the
          top middle.
        </li>
      </ul>
    </div>
  );
}

export default Home;
