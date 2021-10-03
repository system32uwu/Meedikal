import React from "react";
import TitleBar from "../titleBar";

interface IProps {}

const HomeAdmin: React.FC<IProps> = () => {
  return (
    <div className="border-2 w-full h-full">
      <TitleBar title="Home"/>
      <div>home admin</div>
    </div>
  );
};

export default HomeAdmin;
