import React from "react";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import { Dashboard } from "./dashboard";
import { Login } from "./login";

interface IProps {}

export const App: React.FC<IProps> = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/app/dashboard">
          <Dashboard />
        </Route>
        <Route path="/app/login">
          <Login />
        </Route>
        <Route component={Dashboard} />
      </Switch>
    </BrowserRouter>
  );
};
