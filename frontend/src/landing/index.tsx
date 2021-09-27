import React from "react";
import { Home } from "./home";
import { Route, Switch, BrowserRouter } from "react-router-dom";

interface IProps {}

export const Landing: React.FC<IProps> = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route>
          <Home path="/" />
        </Route>
      </Switch>
    </BrowserRouter>
  );
};
