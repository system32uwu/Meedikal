import React from "react";
import { Route, Switch, Router } from "react-router-dom";
import Navbar from "./components/navbar";
import { Home, Login, Contact, Plans } from "./meedikalLanding";
import Dashboard from "./meedikalApp";
import Footer from "./components/footer";
import { createBrowserHistory } from "history";

export const history = createBrowserHistory();

interface IProps {}

const App: React.FC<IProps> = () => {
  return (
    <Router history={history}>
      <Switch>
        <Route path="/app">
          <Dashboard />
        </Route>
        <Route path="/">
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
          </Switch>
          <Footer />
        </Route>
      </Switch>
    </Router>
  );
};

export default App;
