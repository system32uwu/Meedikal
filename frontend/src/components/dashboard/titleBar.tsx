import React from "react";

interface IProps {
  title: string;
}

const TitleBar: React.FC<IProps> = ({ title }) => {
  return <div className="w-full text-center">{title}</div>;
};

export default TitleBar;
