import React from "react";
import AdminAppointments from "./admin/appointments";
import HomeAdmin from "./admin/home";

export type DashboardPages = Array<{
  name: string;
  url: string;
  component?: React.FC;
}>;

export const adminPages: DashboardPages = [
  {
    name: "Home",
    url: "",
    component: HomeAdmin,
  },
  {
    name: "Appointments",
    url: "/appointments",
    component: AdminAppointments,
  },
  {
    name: "Users",
    url: "/users",
  },
  {
    name: "Stats",
    url: "/stats",
  },
];

export const patientPages: DashboardPages = [
  {
    name: "Home",
    url: "/home",
  },
  {
    name: "Appointments",
    url: "/appointments",
  },
  {
    name: "Symptoms",
    url: "/symptoms",
  },
  {
    name: "Clinical Signs",
    url: "/clinicalSigns",
  },
  {
    name: "Diseases",
    url: "/diseases",
  },
  {
    name: "Branches",
    url: "/branches",
  },
];

export const medicalPersonnelPages: DashboardPages = [
  {
    name: "Home",
    url: "/home",
  },
  {
    name: "Appointments",
    url: "/appointments",
  },
  {
    name: "Patients",
    url: "/patients",
  },
  {
    name: "Symptoms",
    url: "/symptoms",
  },
  {
    name: "Clinical Signs",
    url: "/clinicalSigns",
  },
  {
    name: "Diseases",
    url: "/diseases",
  },
];
