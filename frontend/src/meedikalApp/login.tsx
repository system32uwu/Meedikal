import React, { FormEvent, useState } from "react";
import { useHistory, Link } from "react-router-dom";
import { Auth, ErrorResponseShape } from "../types";
import { apiCall, setApi } from "../util/request";
import illustration from "../static/healthcare-graphic.png";
import Navbar from "../components/navbar";

interface IProps {}

export const Login: React.FC<IProps> = () => {
  const [ci, setCi] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const { push } = useHistory();
  const [err, setErr] = useState<null | ErrorResponseShape>(null);

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();
    apiCall<Auth>("auth/login", "POST", { ci: ci, password: password })
      .then((res) => {
        let config = {};
        if (process.env.NODE_ENV === "development") {
          config = {
            headers: {
              Authorization: `Bearer ${res.authToken}`,
            },
            withCredentials: true,
          };
        } else {
          config = { withCredentials: true };
        }
        setApi(config);
        push("/app/dashboard");
      })
      .catch((err) => {
        setErr(err);
      });
  };
  return (
    <div className="flex w-full font-overpass flex-col">
      <Navbar />
      <div className="lg:pt-4 flex w-full">
        <div className="flex flex-col w-full">
          <div className="lg:px-8 flex flex-col pt-8 md:pt-0 px-6 lg:pl-16 lg:h-full lg:justify-around">
            <div>
              <p className="text-2xl font-bold">Welcome</p>
              <p className="text-2xs">
                Don't have an account?
                <Link
                  to="/app/register"
                  className="text-turqoise font-bold pl-1"
                >
                  Register
                </Link>
              </p>
            </div>
            <form
              className="w-full lg:w-5/6 lg:flex-wrap pt-4 md:pt-0"
              onSubmit={handleLogin}
            >
              <div className="lg:justify-between">
                <div>
                  <label
                    className="block text-gray-500 font-bold mb-1 md:mb-0 pr-4 focus:bg-transparent"
                    htmlFor="ci"
                  >
                    ID
                  </label>
                </div>
                <div>
                  <input
                    className="appearance-none border border-gray-300 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:ring-2 focus:ring-turqoise focus:border-turqoise"
                    id="ci"
                    type="text"
                    autoFocus
                    placeholder="X.XXX.XXX-X"
                    value={ci}
                    onChange={(ev) => setCi(ev.target.value)}
                  />
                </div>
              </div>
              <div className="mt-4">
                <div>
                  <label
                    className="text-gray-500 font-bold mb-1 md:mb-0 pr-4"
                    htmlFor="inline-password"
                  >
                    Password
                  </label>
                </div>
                <div>
                  <input
                    className="appearance-none border border-gray-300 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:ring-2 focus:ring-turqoise focus:border-turqoise"
                    id="inline-password"
                    type="password"
                    placeholder="**********"
                    onChange={(ev) => setPassword(ev.target.value)}
                  />
                </div>
              </div>
              {err ? (
                <div>
                  <p className="text-red-500 font-semibold">{err.error}</p>
                </div>
              ) : null}
              <div className="mt-4 text-right">
                <Link to="/app/forgot" className="text-turqoise">
                  Forgot your password?
                </Link>
              </div>
              <div className="mt-4">
                <button
                  className="focus:outline-none shadow bg-turqoise focus:shadow-outline text-white font-bold py-2 px-4 rounded w-full"
                  type="submit"
                >
                  Log In
                </button>
              </div>
            </form>
          </div>
        </div>
        <div className="hidden lg:flex lg:my-auto lg:display-flex lg:mb-4">
          <img src={illustration} alt="hospital illustration" />
        </div>
      </div>
    </div>
  );
};
