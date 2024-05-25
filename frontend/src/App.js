import { Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Home from "./pages/Home";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import Categories from "./pages/Categories";
import CreatePost from "./components/CreatePost";
import UserProfile from "./pages/UserProfile";

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

          <Route path="*" element={<NotFound />} />

        </Route>
      </Routes>

      <ToastContainer />
    </>
  );
}

export default App;
