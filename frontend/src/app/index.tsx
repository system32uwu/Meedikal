import React from "react";
import { RouteComponentProps, Router } from "@reach/router";
import { Dashboard } from "./dashboard";

interface IProps extends RouteComponentProps {}

export const AppRouter: React.FC<IProps> = () => {
  return (
    <Router>
      <Dashboard path="/" />
    </Router>
  );
};
