import React, { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { api, refreshapi } from "@/api/interceptor";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decodedUser = jwtDecode(token);
        setIsAuthenticated(true);
        setUser(decodedUser);

        const isTokenExpired = decodedUser.exp * 1000 < Date.now();
        if (isTokenExpired) {
          handleTokenRefresh();
        } else {
          setLoading(false);
        }

        const interval = setInterval(() => {
          const token = localStorage.getItem("access_token");
          if (token) {
            const decodedUser = jwtDecode(token);
            const timeRemaining = decodedUser.exp * 1000 - Date.now();
            if (timeRemaining < 5 * 60 * 1000) {
              handleTokenRefresh();
            }
          }
        }, 60 * 1000);

        return () => clearInterval(interval);
      } catch (error) {
        console.error("Invalid token", error);
        logout();
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const handleTokenRefresh = async () => {
    try {
      const { data } = await refreshapi.post("/auth/refresh");
      localStorage.setItem("access_token", data.access_token);
      const decodedUser = jwtDecode(data.access_token);
      setIsAuthenticated(true);
      setUser(decodedUser);
    } catch (error) {
      console.error("Failed to refresh token", error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (token) => {
    localStorage.setItem("access_token", token);
    setIsAuthenticated(true);
    const decodedUser = jwtDecode(token);
    setUser(decodedUser);
    navigate("/dashboard");
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsAuthenticated(false);
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        setIsAuthenticated,
        user,
        login,
        logout,
        loading
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
