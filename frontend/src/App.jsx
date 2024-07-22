import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./contexts/authcontext";
import Index from "./pages/Index";
import Signup from "./pages/auth/Signup";
import Login from "./pages/auth/Login";

const Register = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  return <Signup />;
};
function App() {
  return (
    <>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/home" element={<Index />} />
            <Route path="/signup" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
