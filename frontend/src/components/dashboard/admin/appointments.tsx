import React from "react";
import TitleBar from "../titleBar";

interface IProps {}

const AdminAppointments: React.FC<IProps> = () => {
  return (
    <div className="border-2 w-full h-full">
      <TitleBar title="Appointments" />
      <div>admin appointments</div>
    </div>
  );
};

export default AdminAppointments;
