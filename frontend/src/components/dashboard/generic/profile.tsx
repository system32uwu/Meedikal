import React, { useEffect, useState } from "react";
import { useUserStore } from "../../../stores/user";
import { Dictionary } from "../../../types";
import { apiCall } from "../../../util/request";
import { Chip } from "../../common/chip";

const RoleColors: Dictionary<string> = {
  administrative: "bg-red-500",
};

interface IProps {}

interface IUserFieldProps {
  name: string;
  _key: string;
  readOnly?: boolean;
}

const UserField: React.FC<IUserFieldProps> = ({ name, _key, readOnly }) => {
  const { user, setUser } = useUserStore();
  const [value, setValue] = useState<string>(user?.user[_key] || "");
  
  return (
    <div className="flex">
      <span className="text-sm border bg-blue-50 font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">
        {name}
      </span>
      <input
        className="px-4 border-l-0 focus:outline-none focus:ring-1 ring-turqoise rounded-md shadow-sm w-4/6"
        type="text"
        value={value}
        readOnly={readOnly}
        onChange={(e) => {
          setValue(e.target.value);
          setUser({
            ...user,
            user: {
              ...user!.user,
              _key: e.target.value,
            },
          });
        }}
      />
    </div>
  );
};

export const Profile: React.FC<IProps> = () => {
  const { user, undo } = useUserStore();

  useEffect(() => {}, [user]);

  return (
    <div>
      <div className="bg-white rounded-xl flex flex-col">
        <div className="w-64 lg:w-96 self-center">
          <div className="flex flex-col justify-between h-full w-full">
            <div className="shadow-xl flex flex-col w-full py-1 space-y-1">
              <img
                src={
                  user?.user.photoUrl ||
                  "https://res.cloudinary.com/dboafhu31/image/upload/v1625318266/imagen_2021-07-03_091743_vtbkf8.png"
                }
                className="w-full h-full md:w-44 md:h-44 m-auto px-2 md:px-0"
                alt="user profile pic"
              />
              {user?.roles?.map((r) => (
                <Chip
                  key={r}
                  text={r}
                  bold
                  textColor="white"
                  bgColor={RoleColors[`${r}`]}
                />
              ))}
            </div>
          </div>
        </div>
        <div className="shadow-xl p-4 space-y-2">
          <UserField _key="ci" name="ID" readOnly />
          <UserField _key="name1" name="1st Name" />
          <UserField _key="name2" name="2nd Name" />
          <UserField _key="surname1" name="1st Surname" />
          <UserField _key="surname2" name="2nd Surname" />
          <UserField _key="sex" name="Sex" />
          <UserField _key="genre" name="Genre" />
          <UserField _key="birthdate" name="Birthdate" />
          <UserField _key="email" name="Email" />
          <UserField _key="location" name="Location" />
          <div className="flex">
            <span className="text-sm border bg-blue-50 font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">
              Phone Numbers
            </span>
            <div className="flex flex-wrap justify-start">
              {user?.phoneNumbers?.map((p) => (
                <Chip
                  key={p.phone}
                  text={p.phone}
                  btn
                  onClick={() => {
                    apiCall("/user/phoneNumbers", "DELETE", {
                      userPhone: [p],
                    });
                  }}
                />
              ))}
            </div>
          </div>
        </div>
        <div className="mb-4 mt-4 flex justify-between">
          <button
            onClick={() => {
              console.log("cancelling changes");
              undo!;
            }}
            className="bg-red-500 w-96 font-bold text-white text-center text-sm rounded-full py-2"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              console.log("saving changes!");
              console.log(user);
            }}
            className="bg-turqoise w-96 font-bold text-white text-center text-sm rounded-full py-2"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};
