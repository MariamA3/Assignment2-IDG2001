import React, { createContext, useContext, useState, useEffect } from "react";
import axiosInstance from "../api/axios";

// Initialize the Authentication Context
const AuthContext = createContext();

// Custom hook for consuming context easily throughout the application
export function useAuth() {
  return useContext(AuthContext);
}

// The provider component manages the authentication state and provides it to child components
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  // Effect to verify user's session on component mount
  useEffect(() => {
    // Asynchronously verify if a user's session is still valid when the app loads
    const verifySession = async () => {
      setIsLoading(true); // Begin loading state
      try {
        const response = await axiosInstance.get("/api/auth/verify");
        // If verification is successful, set the current user
        setCurrentUser(response.data);
      } catch (error) {
        // Log and handle any verification error
        console.error("Session verification failed:", error);
        setCurrentUser(null); // No valid session, set current user to null
      } finally {
        setIsLoading(false); // End loading state
      }
    };

    verifySession();
  }, []);

  // Function to handle user login
  const login = async ({ email, password }) => {
    try {
      const response = await axiosInstance.post("/api/auth/login", {
        email,
        password,
      });
      // On successful login, update the current user state
      setCurrentUser(response.data.data);
    } catch (error) {
      // Handle login errors and log them
      const errorMessage =
        error.response?.data?.message ||
        "Login failed. Please try again later.";
      console.error("Error during login:", errorMessage);
    }
  };

  // Function to handle user logout
  const logout = async () => {
    try {
      await axiosInstance.post("/api/auth/logout");
      setCurrentUser(null); 
    } catch (error) {
      // Handle logout errors and log them
      const errorMessage = "Error logging out. Please try again.";
      console.error("Logout Error:", errorMessage);
    }
  };

  // Values to be provided through the context
  const value = {
    currentUser,
    isAuthenticated: !!currentUser, 
    login,
    logout,
  };

  // Conditionally render children or a loading indicator based on the loading state
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
