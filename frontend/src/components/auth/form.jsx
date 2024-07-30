import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { loginUser, signupUser } from "@/api/interceptor";
import { useToast } from "@/contexts/toastcontext";
import { AuthContext } from "@/contexts/authcontext";
import Loader from "../Loader";

const Form = ({ formType }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    password: "",
  });
  const { showSuccessToast, showErrorToast } = useToast();
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGoogleAuth = () => {
    window.location.href =
      "http://localhost:5000/auth/authorize/google";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      if (formType === "signup") {
        await signupUser(formData.fullname, formData.email, formData.password);
        showSuccessToast("Signup successful!", {
          duration: 4000,
          position: "top-right",
        });
        navigate("/login");
      } else if (formType === "login") {
        const response = await loginUser(formData.email, formData.password);
        login(response.access_token);
        showSuccessToast(response.message, {
          duration: 4000,
          position: "top-right",
        });
        navigate("/home");
      }
    } catch (error) {
      setError(error.message);
      showErrorToast("Please try again!", {
        duration: 4000,
        position: "top-center",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mx-auto max-w-sm mt-24">
      <CardHeader>
        <CardTitle className="text-2xl">
          {formType === "signup"
            ? "Welcome👋 Create an account to continue!"
            : "Hey there👋, welcome back!"}
        </CardTitle>
        <CardDescription>
          {formType === "signup"
            ? "Sign up so you don't miss the revolution."
            : "Hey there, welcome back!"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button onClick={handleGoogleAuth} variant="outline" className="w-full">
          {formType === "signup" ? "Signup" : "Login"} with Google
        </Button>
        <p>OR</p>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4">
            {formType === "signup" && (
              <div className="grid gap-2">
                <Label htmlFor="fullname">Fullname</Label>
                <Input
                  id="fullname"
                  name="fullname"
                  type="text"
                  placeholder="fullname"
                  value={formData.fullname}
                  onChange={handleChange}
                  required
                />
              </div>
            )}
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                {formType === "login" && (
                  <Link
                    to="/forgot-password"
                    className="ml-auto inline-block text-sm hover:underline"
                  >
                    Forgot your password?
                  </Link>
                )}
              </div>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="********"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <Loader loading={isLoading} />
              ) : formType === "signup" ? (
                "Sign Up"
              ) : (
                "Login"
              )}
            </Button>
          </div>
          <div className="mt-4 text-center text-sm">
            {formType === "signup" ? (
              <>
                Already have an account?{" "}
                <Link to="/login" className="underline">
                  Log in
                </Link>
              </>
            ) : (
              <>
                Don&apos;t have an account?{" "}
                <Link to="/signup" className="underline">
                  Sign up
                </Link>
              </>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default Form;
