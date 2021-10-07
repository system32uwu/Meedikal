import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { useUserStore } from "../../stores/user";
import bell from "../../static/bell.svg";
import userPlaceholder from "../../static/user.svg";
import { history } from "../../App";

const TitleBar: React.FC = () => {
  const { location } = useHistory();
  const [title, setTitle] = useState<string>("Home");
  const { user } = useUserStore();

  useEffect(() => {
    let _title: string | null = location.pathname.split("/app/", 2)[1];
    try {
      _title = _title.charAt(0).toUpperCase() + _title.slice(1);
      _title = _title.replace("/", " - ");
    } catch {
      _title = null;
    } finally {
      setTitle(_title || "Home");
    }
  }, [location, setTitle]);

  return (
    <div className="w-full bg-turqoise h-10 pt-2 flex flex-grow">
      <div className="flex lg:ml-64 w-full">
        <div className="flex flex-row w-full justify-center">
          <p className="absolute text-center text-white font-bold subpixel-antialiased">
            {title}
          </p>
          <div className="justify-end float-right right-0 px-2 flex flex-row space-x-2 w-full">
            <button className="z-10 w-6 h-6 rounded-full bg-white p-0.5">
              <img src={bell} alt="bell" />
            </button>
            <button
              className="z-10 w-6 h-6 rounded-full bg-white"
              onClick={() => history.push("/app/profile")}
            >
              <img
                src={user?.user.photoUrl || userPlaceholder}
                className="object-cover p-1"
                alt="user avatar"
              />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TitleBar;
