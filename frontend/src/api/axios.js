import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Create an axios instance
const axiosInstance = axios.create({
  baseURL: BASE_URL, 
  headers: { "Content-Type": "application/json" }, 
  withCredentials: true,
});

export default axiosInstance;
