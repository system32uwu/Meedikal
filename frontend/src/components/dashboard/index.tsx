import React from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";
import { useUserStore } from "../../stores/user";
import {
  adminPages,
  DashboardPages,
  medicalPersonnelPages,
  patientPages,
} from "./pages";
import { Sidebar } from "./sidebar";

interface IProps {}

export const Dashboard: React.FC<IProps> = () => {
  const { currentRole } = useUserStore();

  switch (currentRole) {
    case "administrative":
      return <UserBoard pages={adminPages} />;
    case "patient":
      return <UserBoard pages={patientPages} />;
    case "medicalPersonnel":
    case "doctor":
    case "medicalAssistant":
      return <UserBoard pages={medicalPersonnelPages} />;
    default:
      return null;
  }
};

const UserBoard: React.FC<{ pages: DashboardPages }> = ({ pages }) => {
  const match = useRouteMatch();

  return (
    <div className="flex h-screen w-screen">
      <Sidebar pages={pages} />
      <div className="flex-wrap w-full gap-x-4 h-full">
        <Switch>
          {pages.map((p) => (
            <Route
              exact
              path={`${match.path}${p.url}`}
              key={p.name}
              component={p.component}
            />
          ))}
        </Switch>
      </div>
    </div>
  );
};
