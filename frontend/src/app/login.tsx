import React, { FormEvent, useState } from "react";
import { useHistory } from "react-router-dom";
import logo from "../static/healthcare-graphic.png";
import { ErrorResponseShape } from "../types";

interface IProps {}

export const Login: React.FC<IProps> = ({}) => {
  const [ci, setCi] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const { push } = useHistory();
  const [err, setErr] = useState<null | ErrorResponseShape>(null);

  const handleLogin = (event: FormEvent) => {
    event.preventDefault();
    fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ ci: ci, password: password }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        res.json().then((data) => {
          if (res.ok) {
            push("/app/dashboard");
          } else {
            console.log(res.status, data);
            setErr(data);
          }
        });
      })
      .catch((e) => console.log(e));
  };
  return (
    <div className="flex w-full font-overpass">
      <div className="lg:pt-14 flex w-full">
        <div className="flex flex-col w-full">
          <div className="flex flex-col pt-8 md:pt-0 px-6 lg:pl-16 lg:h-full lg:justify-around">
            <div>
              <p className="text-4xl font-extrabold">Welcome</p>
              <p className="text-2xs">
                Don't have an account?
                <a href="#" className="text-turqoise font-bold pl-1">
                  Register
                </a>
              </p>
            </div>
            <form className="w-full lg:flex-wrap" onSubmit={handleLogin}>
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
                    className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                    id="ci"
                    type="text"
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
                    className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
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
                <a href="#" className="text-turqoise">
                  Forgot your password?
                </a>
              </div>
              <div className="mt-4">
                <input
                  className="shadow bg-purple-500 hover:bg-purple-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded w-full"
                  type="submit"
                  value="Log In"
                />
              </div>
            </form>
          </div>
        </div>
        <div className="hidden lg:flex lg:my-auto lg:display-flex w-4/5">
          <img src={logo} />
        </div>
      </div>
    </div>
  );
};
