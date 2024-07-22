import React, { createContext, useContext } from "react";
import { Toaster, toast } from "react-hot-toast";

const ToastContext = createContext();

export const useToast = () => useContext(ToastContext);

export const ToastProvider = ({ children }) => {
  const showToast = (message, options) => {
    toast(message, options);
  };
  const showSuccessToast = (message, options) => {
    toast.success(message, options);
  };
  const showErrorToast = (message, options) => {
    toast.error(message, options);
  };

  return (
    <ToastContext.Provider
      value={{ showToast, showSuccessToast, showErrorToast }}
    >
      <Toaster reverseOrder={false} />
      {children}
    </ToastContext.Provider>
  );
};
