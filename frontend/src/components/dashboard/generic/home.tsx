import React from "react";
import { DashboardPage, DashboardPages } from "../pages";

interface IProps {
  pages: DashboardPages;
}

const Home: React.FC<IProps> = ({ pages }) => {
  return (
    <div className="w-full h-full flex flex-wrap px-2 lg:px-4 place-content-around">
      {pages.map((p) => {
        if (p.name !== "Home") {
          return <Card key={p.url} page={p} />;
        }
      })}
    </div>
  );
};

interface CardProps {
  page: DashboardPage;
}

const Card: React.FC<CardProps> = ({ page }) => {
  return (
    <div className="bg-gray-300 text-hard-blue w-32 h-32 lg:w-56 lg:h-56 m-4 flex">
      <div className="self-end text-center w-full py-4">{page.name}</div>
    </div>
  );
};

export default Home;
