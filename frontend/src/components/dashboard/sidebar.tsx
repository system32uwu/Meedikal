import React from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { DashboardPages } from "./pages";
import companyLogo from "../../static/company-logo.png";
interface IProps {
  pages: DashboardPages;
}

export const Sidebar: React.FC<IProps> = ({ pages }) => {
  const match = useRouteMatch();
  return (
    <div className="pr-4 px-2 h-screen bg-pastel-skyblue w-60">
      <div className="h-full w-full divide-y-2 divide-hard-blue">
        <div className="pt-4 grid justify-items-stretch">
          <img
            src={companyLogo}
            alt="company logo"
            className="rounded-full w-20 justify-self-center"
          />
          <p className="text-xs text-center pb-2 pt-1 text-hard-blue font-semibold">
            Healthcare Company
          </p>
        </div>
        <div className="pt-2">
          {pages.map((p) => (
            <Link
              to={`${match.path}${p.url}`}
              key={p.name}
              className="block text-hard-blue font-bold py-2"
            >
              {p.name}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};
