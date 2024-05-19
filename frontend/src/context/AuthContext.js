import React, { createContext, useContext, useState, useEffect } from "react";
import axiosInstance from "../api/axios";
import Loading from "../components/Loading";

// Initialize the Authentication Context
const AuthContext = createContext();

// Custom hook for consuming context easily throughout the application
export function useAuth() {
  return useContext(AuthContext);
}

// The provider component manages the authentication state and provides it to child components
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Effect to verify user's session on component mount
  useEffect(() => {
    // Asynchronously verify if a user's session is still valid when the app loads
    const verifySession = async () => {
      setIsLoading(true); // Begin loading state
      try {
        const response = await axiosInstance.get("/profile");
        // If verification is successful, set the current user
        setCurrentUser(response.data);
        setIsAuthenticated(true);
      } catch (error) {
        // Log and handle any verification error
        console.error("Session verification failed:", error);
        setCurrentUser(null); // No valid session, set current user to null
      } finally {
        setIsLoading(false); // End loading state
      }
    };

    verifySession();
  }, [isAuthenticated]);

  useEffect(() => {
    if (!isLoading) {
      console.log("Current user:", currentUser);
      console.log("Authenticated:", isAuthenticated);
    }
  }, [currentUser, isAuthenticated, isLoading]);

  // Function to handle user login
  const login = async ({ username, password }) => {
    try {
      const response = await axiosInstance.post("/login", {
        username,
        password,
      });
      // On successful login, update the current user and authentication state
      setCurrentUser(response.data.data);
      setIsAuthenticated(true);
    } catch (error) {
      // Handle login errors and log them
      const errorMessage =
        error.response?.data?.message ||
        "Login failed. Please try again later.";
      console.error("Error during login:", errorMessage);
    }
  };

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }

  // Function to handle user logout
  const logout = async () => {
    try {
      await axiosInstance.post(
        "/logout",
        {},
        {
          headers: {
            "X-CSRF-TOKEN": getCookie("csrf_access_token"), // replace 'csrf_access_token' with the name of your CSRF cookie if it's different
          },
          withCredentials: true,
        }
      );
      // On successful logout, update the current user and authentication state
      setCurrentUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      // Handle logout errors and log them
      const errorMessage = "Error logging out. Please try again.";
      console.error("Logout Error:", errorMessage);
    }
  };

  // Values to be provided through the context
  const value = {
    currentUser,
    isAuthenticated,
    isLoading,
    login,
    logout,
  };

  // Conditionally render children or a loading indicator based on the loading state
  return (
    <AuthContext.Provider value={value}>
      {isLoading ? <Loading /> : children}
    </AuthContext.Provider>
  );
};
