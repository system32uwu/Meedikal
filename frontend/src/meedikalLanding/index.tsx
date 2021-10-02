import React from "react";
import { Home } from "./home";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import { NotFound } from "../components/notFound";
import Navbar from "../components/navbar";

interface IProps {}

const MeedikalLanding: React.FC<IProps> = () => {
  return (
    <div>
      <Navbar />
      <BrowserRouter>
        <Switch>
          <Route path="/">
            <Home />
          </Route>
          <Route component={NotFound} />
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default MeedikalLanding;
