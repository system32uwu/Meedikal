import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import companyLogo from "../static/company-logo.png";

interface IProps {}

const MenuItems = [
  {
    label: "Home",
    url: "/",
  },
  {
    label: "Contact",
    url: "/contact",
  },
  {
    label: "Plans",
    url: "/plans",
  },
];

const Navbar: React.FC<IProps> = () => {
  const [menu, toggleMenu] = useState<boolean>(false);
  const { pathname } = useLocation();
  return (
    <nav className="bg-white shadow font-overpass">
      <div className="container px-6 py-4 mx-auto md:flex md:justify-between md:items-center">
        <div className="flex items-center justify-between">
          <div className="flex flex-row">
            <Link
              className="flex flex-row focus:outline-none text-md font-thin text-gray-800 lg:text-2xl self-end text-turqoise"
              to="/"
            >
              <img
                src={companyLogo}
                alt="company logo"
                className="rounded-full w-10 mr-2"
              />
              <p className="text-center self-center">Healthcare Company</p>
            </Link>
          </div>

          <div className="flex md:hidden">
            <button
              type="button"
              className="text-gray-500 hover:text-turqoise focus:outline-none focus:text-gray-600 self-center"
              aria-label="toggle menu"
              onClick={() => toggleMenu(!menu)}
            >
              <svg viewBox="0 0 24 24" className="w-6 h-10 fill-current">
                <path
                  fillRule="evenodd"
                  d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
                ></path>
              </svg>
            </button>
          </div>
        </div>

        <div className={"items-center md:flex " + (menu ? "block" : "hidden")}>
          <div className="flex flex-col md:flex-row md:mx-6">
            {MenuItems.map((item) => (
              <Link
                to={item.url}
                key={item.label}
                className={
                  "my-1 text-sm font-medium text-gray-700 hover:text-turqoise md:mx-4 md:my-0 " +
                  (pathname === item.url ? "text-turqoise" : "")
                }
              >
                {item.label}
              </Link>
            ))}
            {pathname === "/login" ? (
              <Link
                to={"/register"}
                className="my-1 text-sm font-medium text-gray-700 hover:text-turqoise md:mx-4 md:my-0"
              >
                Register
              </Link>
            ) : (
              <Link
                to={"/login"}
                className="my-1 text-sm font-medium text-gray-700 hover:text-turqoise md:mx-4 md:my-0"
              >
                Log In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
