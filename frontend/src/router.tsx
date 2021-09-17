import React from "react";
import { Router } from "@reach/router";
import { LandingRouter } from "./landing";
import { AppRouter } from "./app";

interface IProps {}

const App: React.FC<IProps> = () => {
  return (
    <Router>
      <LandingRouter path="/" />
      <AppRouter path="/app" />
    </Router>
  );
};

export default App;
