import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/GoBack.css";

// Will be used for all for buttons that go back to the previous page
const GoBackButton = ({ children }) => {
  const navigate = useNavigate();

  const handleGoBack = (event) => {
    event.preventDefault();
    navigate(-1);
  };

  return <button className="goBack" onClick={handleGoBack}>{children}</button>;
};

export default GoBackButton;
