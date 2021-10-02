import React, { useState } from "react";
import companyLogo from "../static/company-logo.png";

interface IProps {}

const Navbar: React.FC<IProps> = () => {
  const [menu, toggleMenu] = useState<boolean>(false);
  return (
    <nav className="bg-white shadow dark:bg-gray-800">
      <div className="container px-6 py-4 mx-auto md:flex md:justify-between md:items-center">
        <div className="flex items-center justify-between">
          <div className="flex flex-row">
            <img src={companyLogo} alt="company logo" className="rounded-full w-10" />
            <a
              className="text-md font-thin text-gray-800 dark:text-white lg:text-2xl self-end pl-2 text-turqoise"
              href="/"
            >
              Healthcare Company
            </a>
          </div>

          <div className="flex md:hidden">
            <button
              type="button"
              className="text-gray-500 dark:text-gray-200 hover:text-turqoise dark:hover:text-gray-400 focus:outline-none focus:text-gray-600 dark:focus:text-gray-400"
              aria-label="toggle menu"
              onClick={() => toggleMenu(!menu)}
            >
              <svg viewBox="0 0 24 24" className="w-6 h-6 fill-current">
                <path
                  fill-rule="evenodd"
                  d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
                ></path>
              </svg>
            </button>
          </div>
        </div>

        <div className={"items-center md:flex " + (menu ? "block" : "hidden")}>
          <div className="flex flex-col md:flex-row md:mx-6">
            <a
              className="my-1 text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-turqoise dark:hover:text-indigo-400 md:mx-4 md:my-0"
              href="/"
            >
              Home
            </a>
            <a
              className="my-1 text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-turqoise dark:hover:text-indigo-400 md:mx-4 md:my-0"
              href="/help"
            >
              Help
            </a>
            <a
              className="my-1 text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-turqoise dark:hover:text-indigo-400 md:mx-4 md:my-0"
              href="/contact"
            >
              Contact
            </a>
            <a
              className="my-1 text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-turqoise dark:hover:text-indigo-400 md:mx-4 md:my-0"
              href="/app/register"
            >
              Register
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
