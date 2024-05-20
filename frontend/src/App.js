import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import Categories from "./pages/Categories";
import CreatePost from "./components/CreatePost";
import UserProfile from "./pages/UserProfile";
import SecureRoute from "./components/AuthRoutes";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/" element={<Home />} />

          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/u/:username" element={<UserProfile />} />

          <Route path="/b/:categoryName" element={<Categories />} />
          <Route path="/b/:categoryName/:categoryId" element={<CreatePost />} />

          {/* SecureRoute is a custom component that checks if the user is authenticated dont know if 
          we need to actual use it i have made it so that certain components are only rendered if the 
          user i authenticated */}
          <Route element={<SecureRoute />}>
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
