import { api } from "@/api/interceptor";
import React, { useRef, useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

const CheckoutButton = ({ onSuccess, duration = 3000 }) => {
  const [pressing, setPressing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [note, setNote] = useState("");
  const timeoutRef = useRef(null);

  useEffect(() => {
    if (pressing) {
      const start = Date.now();
      timeoutRef.current = setInterval(() => {
        const elapsed = Date.now() - start;
        setProgress((elapsed / duration) * 100);
        if (elapsed >= duration) {
          clearInterval(timeoutRef.current);
          handleSuccess();
        }
      }, 100);
    } else {
      clearInterval(timeoutRef.current);
      setProgress(0);
    }

    return () => clearInterval(timeoutRef.current);
  }, [pressing]);

  const handleSuccess = async () => {
    try {
      const response = await api.post("/checkouts/create", { note });
      if (onSuccess) onSuccess(response.data);
    } catch (error) {
      console.error("Error creating checkout:", error);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto border-0">
      <CardHeader>
        <CardTitle>Safe Return Confirmation</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label htmlFor="note" className="block text-left text-sm font-medium text-gray-700 mb-1">
            Add a note (required):
          </label>
          <Textarea
            id="note"
            placeholder="e.g., Meeting friends at the park"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            className="w-full"
            disabled={pressing}
            required
          />
        </div>
        <div className="text-sm text-gray-600 mb-4">
          Hold the button below to confirm your safe return home.
        </div>
        <div className="relative">
          <Button
            className="relative w-full h-12 bg-gray-600 hover:bg-gray-700 text-white rounded overflow-hidden"
            onMouseDown={() => setPressing(true)}
            onMouseUp={() => setPressing(false)}
            onMouseLeave={() => setPressing(false)}
            onTouchStart={() => setPressing(true)}
            onTouchEnd={() => setPressing(false)}
          >
            Hold to Confirm Safe Return
            {pressing && (
              <div
                className="absolute top-0 left-0 h-full bg-gray-800"
                style={{ width: `${progress}%`, transition: "width 0.1s linear" }}
              />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CheckoutButton;