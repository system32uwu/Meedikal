import React from "react";

interface IProps {
  title: string;
}

const TitleBar: React.FC<IProps> = ({ title }) => {
  return (
    <div className="w-full text-center bg-turqoise text-white h-8 py-1 font-bold subpixel-antialiased">
      {title}
    </div>
  );
};

export default TitleBar;
