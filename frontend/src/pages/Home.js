import GetPosts from "../components/GetPosts";
import "../styles/Home.css";

function Home() {
    return (
        <div className="home-container">
            <h2>Home</h2>
            <p>Recent posts:</p>
            {/* Here vi can insert the posts for a category */}
            {/* I dont know which one we should show when the user first load*/}
            <GetPosts />
        </div>
    );
}

export default Home;