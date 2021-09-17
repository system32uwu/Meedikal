import React from "react";
import { RouteComponentProps, Router } from "@reach/router";
import { Home } from "./home";

interface IProps extends RouteComponentProps {}

export const LandingRouter: React.FC<IProps> = () => {
  return (
    <Router>
      <Home path="/" />
    </Router>
  );
};
