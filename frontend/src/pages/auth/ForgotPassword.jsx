import React, { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/contexts/toastcontext";
import { api } from "@/api/interceptor";
import Loader from "@/components/Loader";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [isDisabled, setIsDisabled] = useState(false)
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { showSuccessToast, showErrorToast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.post("/auth/forgot-password", {
        email,
      });
      showSuccessToast("Password reset link sent to your email", {
        duration: 4000,
        position: "top-center",
      });
      setEmail("")
    } catch (error) {
      if (error.message) {
        setError(error.message);
      }
      showErrorToast(error.message || "Failed to send reset link");
    } finally {
      setIsLoading(false);
      setTimeout(()=>{
        setIsDisabled(True)
      }, 4000)
    }
  };

  return (
    <Card className="mx-auto max-w-sm mt-24">
      <CardHeader>
        <CardTitle>Forgot Password</CardTitle>
        <CardDescription>
          Don't forget this new password this time. Please.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                disabled={isDisabled}
                placeholder="Enter your email..."
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button type="submit" disabled={isLoading}>
              {isLoading ? <Loader /> : "Send Reset Link"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default ForgotPassword;
