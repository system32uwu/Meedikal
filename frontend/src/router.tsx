import React from "react";
import { Redirect, Router } from "@reach/router";
import { LandingRouter } from "./landing";
import { AppRouter } from "./app";

interface IProps {}

const App: React.FC<IProps> = () => {
  return (
    <Router>
      <LandingRouter path="/" />
      <AppRouter path="/app" />
      <Redirect noThrow from="/app/*" to="/app" />
      <Redirect noThrow from="*" to="/" />
    </Router>
  );
};

export default App;
