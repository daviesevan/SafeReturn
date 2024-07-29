import { AuthContext } from "@/contexts/authcontext";
import { useToast } from "@/contexts/toastcontext";
import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const GoogleAuth = () => {
  const { login, setIsAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  const { showSuccessToast } = useToast();
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");
    const message = params.get("message");

    if (accessToken && refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
      login(accessToken);
      setIsAuthenticated(true)
      showSuccessToast(message, {
        duration: 4000,
        position: "top-center",
      });
    } else {
      navigate("/home");
    }
  }, [login, navigate]);
  return <div>Authenticating...</div>;
};

export default GoogleAuth;
