import React from "react";
import { useUserStore } from "../../../stores/user";
import { apiCall } from "../../../util/request";
import { Chip } from "../../common/chip";

interface IProps {}

interface IUserFieldProps {
  name: string;
  value: string | undefined | null;
}

const UserField: React.FC<IUserFieldProps> = ({ name, value }) => (
  <div className="flex">
    <span className="text-sm border bg-blue-50 font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">
      {name}
    </span>
    <input
      className="px-4 border-l-0 cursor-default border-gray-300 focus:outline-none  rounded-md rounded-l-none shadow-sm -ml-1 w-4/6"
      type="text"
      value={value || ""}
      readOnly
    />
  </div>
);

export const Profile: React.FC<IProps> = () => {
  const { user, fetch } = useUserStore();

  return (
    <div>
      <div className="md:grid grid-cols-4 bg-white gap-2 rounded-xl">
        <div className="md:col-span-3 shadow-xl p-4 space-y-2">
          <UserField name="ID" value={user?.user.ci.toString()} />
          <UserField name="1st Name" value={user?.user.name1} />
          <UserField name="2nd Name" value={user?.user.name2} />
          <UserField name="1st Surname" value={user?.user.surname1} />
          <UserField name="2nd Surname" value={user?.user.surname2} />
          <UserField name="Sex" value={user?.user.sex} />
          <UserField name="Genre" value={user?.user.genre} />
          <UserField name="Birthdate" value={user?.user.birthdate} />
          <UserField name="Email" value={user?.user.email} />
          <UserField name="Location" value={user?.user.location} />
          <div className="flex">
            <span className="text-sm border bg-blue-50 font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">
              Phone Numbers:
            </span>
            <div className="flex flex-wrap justify-start">
              {user?.phoneNumbers.map((p) => (
                <Chip
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

          <UserField name="Roles" value={user?.roles.join(", ")} />
        </div>
        <div className="md:col-span-1 h-48 shadow-xl ">
          <div className="flex w-full h-full relative">
            <img
              src={
                user?.user.photoUrl ||
                "https://res.cloudinary.com/dboafhu31/image/upload/v1625318266/imagen_2021-07-03_091743_vtbkf8.png"
              }
              className="w-44 h-44 m-auto"
              alt="user profile picture"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
