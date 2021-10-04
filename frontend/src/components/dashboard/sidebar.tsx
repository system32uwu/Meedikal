import React, { useState } from "react";
import { Link, useRouteMatch, useLocation } from "react-router-dom";
import { useUserStore } from "../../stores/user";
import { DashboardPages } from "./pages";
interface IProps {
  pages: DashboardPages;
}

export const Sidebar: React.FC<IProps> = ({ pages }) => {
  const [isSidebarOpen, toggleSidebar] = useState(true);
  const match = useRouteMatch();
  const { pathname } = useLocation();
  const { logout } = useUserStore();

  return (
    <div>
      <div className="relative lg:display-none">
        <button
          type="button"
          className={`text-white top-2 left-2 focus:outline-none focus:text-gray-600 hover:text-gray-600 ${
            !isSidebarOpen ? "absolute" : "hidden"
          }`}
          aria-label="toggle menu"
          onClick={() => toggleSidebar(!isSidebarOpen)}
        >
          <svg viewBox="0 0 24 24" className="w-6 h-6 fill-current">
            <path
              fillRule="evenodd"
              d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
            ></path>
          </svg>
        </button>
      </div>
      <div
        className={`transition-all  duration-500  fixed top-0 ${
          isSidebarOpen ? "left-0" : "-left-64"
        }`}
      >
        <div className="flex h-screen overflow-y-auto flex-col bg-white w-64 px-4 py-8 border-r min-h-screen relative">
          <h2 className="fixed top-2 text-xl font-semibold text-gray-800">
            Healthcare <span className="text-turqoise ml-1">Company</span>
          </h2>
          <button
            onClick={() => toggleSidebar(!isSidebarOpen)}
            className="absolute top-2 right-1  text-gray-600 w-8 h-8 rounded-full flex items-center justify-center active:bg-gray-300 focus:outline-none ml-6 hover:bg-gray-200 hover:text-gray-800"
          >
            <svg viewBox="0 0 24 24" className="w-6 h-6 fill-current">
              <path
                fillRule="evenodd"
                d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
              ></path>
            </svg>
          </button>
          <div className="flex flex-col mt-1  justify-between flex">
            <nav className="text">
              {pages.map((p) => (
                <Link
                  to={`${match.path}${p.url}`}
                  key={p.name}
                  className={`block text-hard-blue font-bold py-2 flex items-start py-2 mt-5 rounded-md hover:text-gray-700 hover:bg-gray-200 transition-colors transform w-full focus:outline-none ${
                    match.path + p.url === pathname ? "bg-gray-200" : ""
                  }`}
                >
                  <span className="mx-4 font-medium">{p.name}</span>
                </Link>
              ))}
              <hr className="my-6" />
              <Link
                to={`${match.path}/settings`}
                className={`block text-hard-blue font-bold flex items-start py-2 mt-5 rounded-md hover:text-gray-700 hover:bg-gray-200 transition-colors transform w-full focus:outline-none ${
                  match.path + "/settings" === pathname ? "bg-gray-200" : ""
                }`}
              >
                {/* <MdSettings className="w-5 h-5" /> */}
                <span className="mx-4 font-medium">Settings</span>
              </Link>
              <button
                className="block text-hard-blue font-bold flex items-start py-2 mt-4 rounded-md hover:text-gray-700 hover:bg-gray-200 transition-colors transform w-full focus:outline-none"
                onClick={() => {
                  logout();
                }}
              >
                {/* <HiTicket className="w-5 h-5" /> */}
                <span className="mx-4 font-medium">Log out</span>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};
