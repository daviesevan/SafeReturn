import { Settings2 } from "lucide-react";
import React from "react";
import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <section className="text-center flex flex-col justify-center items-center h-96 mt-20">
      <Settings2 className="h-24 w-24 text-gray-900 text-6xl mb-4" />
      <h1 className="text-6xl font-bold mb-4">404 Not Found</h1>
      <p className="text-xl mb-5">This page does not exist</p>
      <Link
        to="/home"
        className="text-white bg-gray-700 hover:bg-gray-900 rounded-md px-3 py-2 mt-4"
      >
        Go Back
      </Link>
    </section>
  );
};

export default NotFoundPage;
