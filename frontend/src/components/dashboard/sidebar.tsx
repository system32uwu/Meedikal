import React from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { DashboardPages } from "./pages";

interface IProps {
  pages: DashboardPages;
}

export const Sidebar: React.FC<IProps> = ({ pages }) => {
  const match = useRouteMatch();
  return (
    <div className="pr-4 px-2 h-screen border-2">
      <div className="h-full">
        {pages.map((p) => (
          <Link to={`${match.path}${p.url}`} key={p.name} className="block">
            {p.name}
          </Link>
        ))}
      </div>
    </div>
  );
};
