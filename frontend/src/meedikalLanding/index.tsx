import React from "react";
import { Home } from "./home";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import { NotFound } from "../components/notFound";
import Navbar from "../components/navbar";
import Contact from "./contact";
import { Login } from "./login";
import Plans from "./plans";

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
          <Route exact path="/login">
            <Login />
          </Route>
          <Route exact path="/plans">
            <Plans />
          </Route>
          <Route component={NotFound} />
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default MeedikalLanding;
