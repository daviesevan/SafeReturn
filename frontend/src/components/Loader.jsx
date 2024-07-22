import React from "react";
import { BarLoader } from "react-spinners";

// const override = {
//   display: "block",
//   margin: "100px auto",
// };

const Loader = ({ loading }) => {
  return (
    <div>
      <BarLoader
        height={4}
        width={100}
        size={150}
        loading={loading}
        color="#fff"
        // cssOverride={override}
      />
    </div>
  );
};

export default Loader;
