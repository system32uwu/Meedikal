import React from "react";
import Home from "../generic/home";
import { adminPages } from "../pages";

interface IProps {}

const HomeAdmin: React.FC<IProps> = () => {
  return (
    <div className="w-full h-full">
      <Home pages={adminPages}/>
    </div>
  );
};

export default HomeAdmin;
