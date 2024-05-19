import "../styles/Home.css";

function Home() {
    return (
        <div className="home-container">
            <h2>Home</h2>
            {/* Here vi can insert the posts for a category */}
            {/* I dont know which one we should show when the user first load*/}
            {/* Maybe just have a recent posts that fetches the most recent post made */}
            <h3>Welcome to breadit!</h3>
            <p>Select one of the categories on the sidebar to get started!</p>
            <p>If you want to post your own content go into one of the categories and start posting!</p>
        </div>
    );
}

export default Home;