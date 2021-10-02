import React from "react";
import { Home } from "./home";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import { NotFound } from "../components/notFound";
import Navbar from "../components/navbar";
import Contact from "./contact";

interface IProps {}

const MeedikalLanding: React.FC<IProps> = () => {
  return (
    <div>
      <BrowserRouter>
        <Navbar />
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route exact path="/contact">
            <Contact />
          </Route>
          <Route component={NotFound} />
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default MeedikalLanding;
