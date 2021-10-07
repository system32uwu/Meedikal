import React from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";
import { useUserStore } from "../../stores/user";
import { Profile } from "./generic/profile";
import {
  adminPages,
  DashboardPages,
  medicalPersonnelPages,
  patientPages,
} from "./pages";
import { Sidebar } from "./sidebar";
import TitleBar from "./titleBar";

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
    <div className="flex">
      <Sidebar pages={pages} />
      <div className="flex-wrap w-full h-full">
        <TitleBar />
        <div className="lg:ml-64"> {/* size of sidebar */}
          <Switch>
            {pages.map((p) => (
              <Route
                exact
                path={`${match.path}${p.url}`}
                key={p.name}
                component={p.component}
              />
            ))}
            <Route exact path={`${match.path}/profile`}>
              <Profile />
            </Route>
          </Switch>
        </div>
      </div>
    </div>
  );
};
