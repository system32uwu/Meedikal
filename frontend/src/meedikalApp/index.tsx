import React from "react";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import { Dashboard } from "./dashboard";

interface IProps {}

const MeedikalApp: React.FC<IProps> = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/app/dashboard">
          <Dashboard />
        </Route>
        <Route component={Dashboard} />
      </Switch>
    </BrowserRouter>
  );
};

export default MeedikalApp;
